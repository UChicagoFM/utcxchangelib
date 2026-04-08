import grpc
from grpc import aio
import utcxchangelib.service_pb2 as utc_bot_pb2
import utcxchangelib.service_pb2_grpc as utc_bot_pb2_grpc
from enum import Enum
import logging
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Optional, Union
import time
import asyncio

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger("xchange-client")
_LOGGER.setLevel(logging.INFO)


@dataclass
class SwapInfo:
    swap_name: str
    from_info: list
    to_info: list
    cost: int
    is_flat: bool


DEFAULT_SWAP_MAP = {
    "toETF": SwapInfo("toETF", [("A", 1), ("B", 1), ("C", 1)], [("ETF", 1)], 5, True),
    "fromETF": SwapInfo("fromETF", [("ETF", 1)], [("A", 1), ("B", 1), ("C", 1)], 5, True),
}

OPTION_STRIKES = [950, 1000, 1050]
OPTION_SYMBOLS = [
    f"B_{t}_{k}" for k in OPTION_STRIKES for t in ("C", "P")
]

DEFAULT_SYMBOLS = [
    "A", "B", "C", "ETF",
    *OPTION_SYMBOLS,
    "R_CUT", "R_HOLD", "R_HIKE",
]

class Side(Enum):
    BUY = 1
    SELL = 2


@dataclass
class OrderBook:
    bids: dict = field(default_factory=dict)
    asks: dict = field(default_factory=dict)

class XChangeClient:
    """
        A basic bot that can be used to interface with the 2026 UTC Xchange. Participants can
        subclass this bot to implement specific functionality and trading logic.
    """

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        silent: bool = False,
        symbols: Optional[list[str]] = None,
        swap_map: Optional[dict[str, SwapInfo]] = None,
    ):
        """ Initializes the bot
        :param host:        Host server where the exchange is being run
        :param username:    Participant's username
        :param password:    Participant's password
        """
        self.host = host
        self.username = username
        self.password = password
        self.symbols = list(symbols or DEFAULT_SYMBOLS)
        self.swap_map = dict(swap_map or DEFAULT_SWAP_MAP)
        self.positions = defaultdict(int, {symbol: 0 for symbol in self.symbols} | {"cash": 0})
        self.open_orders = dict()
        self.order_books = {sym: OrderBook() for sym in self.symbols}
        self.order_id = int(time.time() * 1000)  # start order id number from time
        self.connected = False
        self.call = None
        self.write_lock = asyncio.Lock()
        if silent:
            _LOGGER.setLevel(logging.WARNING)

    def _ensure_symbol(self, symbol: str) -> None:
        if symbol not in self.order_books:
            self.order_books[symbol] = OrderBook()
        if symbol not in self.positions:
            self.positions[symbol] = 0
        if symbol not in self.symbols:
            self.symbols.append(symbol)

    async def connect(self) -> None:
        """
        Connects to the server using the username and password from initialization. Main loop of the bot that
        processes messages and calls the appropriate message handler.
        :return:
        """
        _LOGGER.info("Connecting to host %s as %s", self.host, self.username)
        channel = aio.insecure_channel(self.host)
        stub = utc_bot_pb2_grpc.ClientStub(channel)
        self.call = stub.Start()

        auth_request = utc_bot_pb2.AuthenticateRequest(username=self.username, password=self.password)
        request = utc_bot_pb2.ClientMessageToExchange(authenticate=auth_request)
        await self.call.write(request)

        while True:
            response = await self.call.read()
            await self.process_message(response)

    async def place_order(self, symbol: str, qty: int, side: Union[Side, str], px: int = None) -> str:
        """ Function to place an order on the exchange. Places a market order if px is none, otherwise a limit order.
        :param symbol: Symbol for the order
        :param qty: Amount to order
        :param side: Buy or sell
        :param px: Price for limit order, if None then submits a market order
        :return: String order id
        """

        _LOGGER.info("Placing Order")
        self._ensure_symbol(symbol)

        if isinstance(side, str):
            side = Side.BUY if side == "buy" else Side.SELL

        side = utc_bot_pb2.NewOrderRequest.Side.BUY if side == Side.BUY else utc_bot_pb2.NewOrderRequest.Side.SELL
        is_market = px is None

        async with self.write_lock:
            if is_market:
                market_order_msg = utc_bot_pb2.MarketOrder(qty=qty)
                order_request = utc_bot_pb2.NewOrderRequest(symbol=symbol, id=str(self.order_id), market=market_order_msg,
                                                            side=side)
            else:
                limit_order_msg = utc_bot_pb2.LimitOrder(qty=qty, px=px)
                order_request = utc_bot_pb2.NewOrderRequest(symbol=symbol, id=str(self.order_id), limit=limit_order_msg,
                                                            side=side)
            request = utc_bot_pb2.ClientMessageToExchange(new_order=order_request)
            await self.call.write(request)
            self.open_orders[str(self.order_id)] = [order_request, qty, is_market]
            self.order_id += 1

            ret = self.order_id - 1

        return str(ret)

    async def place_swap_order(self, swap: str, qty: int) -> None:
        """
        Places a swap request with the exchange.
        :param swap: Name of the swap
        :param qty: Quantity of swaps to execute
        :return:
        """
        _LOGGER.info("Placing Swap Order: %s, qty: %d", swap, qty)
        async with self.write_lock:
            swap_request = utc_bot_pb2.SwapRequest(name=swap, qty=qty)
            request = utc_bot_pb2.ClientMessageToExchange(swap=swap_request)
            await self.call.write(request)

    async def cancel_order(self, order_id: str) -> None:
        """ Places a cancel order request for the given order id
        :param order_id: order_id of the order to cancel
        :return:
        """
        _LOGGER.info("Requesting to cancel order: %s", order_id)
        async with self.write_lock:
            cancel_request = utc_bot_pb2.CancelOrderRequest(id=order_id)
            request = utc_bot_pb2.ClientMessageToExchange(cancel_order=cancel_request)
            await self.call.write(request)

    async def handle_trade_msg(self, msg):
        self._ensure_symbol(msg.symbol)
        await self.bot_handle_trade_msg(msg.symbol, msg.px, msg.qty)

    async def handle_order_fill(self, msg) -> None:
        """
        Updates the positions based on the order fill. Then calls the bot specific code.
        :param msg: OrderFillMessage from exchange
        :return:
        """
        order_info: list = self.open_orders.get(msg.id, [])
        if not order_info:
            _LOGGER.debug("Received fill for order id %s not in open orders - likely due to click trade")
            return

        symbol: str = order_info[0].symbol
        self._ensure_symbol(symbol)
        fill_qty: int = msg.qty
        fill_price: int = msg.px
        is_buy = order_info[0].side == utc_bot_pb2.NewOrderRequest.Side.BUY

        order_info[1] -= fill_qty
        if order_info[1] == 0:
            _LOGGER.info("Order %s Completely Filled (%s %d @ %d)", msg.id, "BUY" if is_buy else "SELL", fill_qty, fill_price)
        else:
            _LOGGER.info("Order %s Partial Filled (%s %d @ %d). %d remaining", msg.id, "BUY" if is_buy else "SELL", fill_qty, fill_price, order_info[1])

        await self.bot_handle_order_fill(msg.id, fill_qty, fill_price)
        # TODO: create an open order dataclass
        if order_info[1] == 0 and not order_info[2]: # do not remove market order
            self.open_orders.pop(msg.id)

    async def handle_order_rejected(self, msg) -> None:
        """
        Calls the users order rejection handler and then removes it from the open orders.
        :param msg: Order Rejected Message
        """
        if msg.id not in self.open_orders:
            return
        await self.bot_handle_order_rejected(msg.id, msg.reason)
        self.open_orders.pop(msg.id)

    async def handle_cancel_response(self, msg):
        """
        Processes a cancel order response and calls the users handler.
        :param msg:
        :return:
        """
        if msg.id not in self.open_orders:
            return
        result_type = msg.WhichOneof('result')
        if result_type == 'ok':
            _LOGGER.info("Cancel order %s successful.", msg.id)
            await self.bot_handle_cancel_response(msg.id, True, None)
            self.open_orders.pop(msg.id)
        else:
            _LOGGER.info("Failed to cancel order %s.", msg.id)
            await self.bot_handle_cancel_response(msg.id, False, msg.error)

    async def handle_swap_response(self, msg) -> None:
        """
        Updates positions if swap was successful.
        :param msg: SwapResponse message from the exchange
        :return:
        """
        swap_request = msg.request
        result_type = msg.WhichOneof('result')
        if result_type == 'ok':
            swap = self.swap_map.get(swap_request.name)
            if swap is None:
                _LOGGER.warning(
                    "Swap '%s' succeeded but is not in swap_map — local positions may be stale. "
                    "Pass the correct swap_map to XChangeClient if you are using custom swaps.",
                    swap_request.name,
                )
            await self.bot_handle_swap_response(swap_request.name, swap_request.qty, True)
        else:
            await self.bot_handle_swap_response(swap_request.name, swap_request.qty, False)
        _LOGGER.info(self.positions)

    async def handle_book_snapshot(self, msg) -> None:
        """
        Update the books based on full snapshot from the exchange.
        :param msg: BookSnapshot message from the exchange
        """
        self._ensure_symbol(msg.symbol)
        book = self.order_books[msg.symbol]
        book.bids = {bid.px: bid.qty for bid in msg.bids}
        book.asks = {ask.px: ask.qty for ask in msg.asks}


        await self.bot_handle_book_update(msg.symbol)

    async def handle_book_update(self, msg) -> None:
        """
        Updates the book based on the incremental updates to the books
        provided by the exchange.
        :param msg: BookUpdate
        """

        self._ensure_symbol(msg.symbol)
        is_bid = msg.side == utc_bot_pb2.BookUpdate.Side.BUY
        book = self.order_books[msg.symbol].bids if is_bid else self.order_books[msg.symbol].asks
        if msg.px not in book:
            book[msg.px] = msg.dq
        else:
            book[msg.px] += msg.dq

        await self.bot_handle_book_update(msg.symbol)

    def handle_position_snapshot(self, msg) -> None:
        """Copy over positions from the exchange records"""
        positions = defaultdict(int)
        _LOGGER.info(msg)
        for position in msg.positions:
            self._ensure_symbol(position.symbol)
            positions[position.symbol] = position.position
        positions['cash'] = msg.cash
        self.positions = defaultdict(int, positions)
        _LOGGER.info("Received Position snapshot from server")
        _LOGGER.info(self.positions)


    async def handle_news_message(self, news_msg):
        """
        Handle news messages and dispatch to appropriate bot handler.
        :param news_msg: NewsMessage
        """
        news_type = 'structured' if news_msg.HasField('structured') else 'unstructured'

        news_release = {
            'tick': news_msg.tick,
            'kind': news_type,
            'symbol': news_msg.symbol if news_msg.HasField('symbol') else None,
        }

        if news_type == "structured":
            subtype = news_msg.structured.WhichOneof("subtype")
            if subtype == "earnings":
                news_release['new_data'] = {
                    "value": news_msg.structured.earnings.value,
                    "asset": news_msg.structured.earnings.asset,
                    "structured_subtype": "earnings"
                }
            elif subtype == "cpi_print":
                news_release['new_data'] = {
                    "forecast": news_msg.structured.cpi_print.forecast,
                    "actual": news_msg.structured.cpi_print.actual,
                    "structured_subtype": "cpi_print",
                }
            else:
                news_release['new_data'] = {"structured_subtype": None}
        else:
            news_release["new_data"] = {
                "content": news_msg.unstructured.content,
                "type": news_msg.unstructured.message_type
            }
        
        await self.bot_handle_news(news_release)

    async def bot_handle_book_update(self, symbol: str) -> None:
        """
        Function for the user to fill in if they want to have any action upon receiving
        book updates.
        # TODO: Fill in subclassed bot.
        :return:
        """
        pass

    async def bot_handle_trade_msg(self, symbol: str, price: int, qty: int):
        """
        Function for the user to fill in if they want to have any action upon receiving
        a TradeMessage.
        # TODO: Fill in subclassed bot.
        :param symbol: Symbol being traded
        :param price: Price at which the trade occured
        :param qty: Quantity traded
        :return:
        """
        pass

    async def bot_handle_order_fill(self, order_id: str, qty: int, price: int):
        """
        Function for the user to fill in if they want to have any additional actions upon receiving
        an OrderFillMessage.
        # TODO: Fill in subclassed bot.
        :param order_id: Order id corresponding to fill
        :param qty: Amount filled
        :param price: Price filled at
        :return:
        """
        pass

    async def bot_handle_order_rejected(self, order_id: str, reason: str) -> None:
        """
        Function for the user to fill in if they want to have any additional actions upon receiving
        an OrderRejectedMessage.
        # TODO: Fill in subclassed bot.
        :param order_id: order id corresponding to the one in open_orders
        :param reason: reason for rejection from the exchange
        """
        pass

    async def bot_handle_cancel_response(self, order_id: str, success: bool, error: Optional[str]) -> None:
        """
        Function for the user to fill in if they want to have any additional actions upon receiving
        a CancelOrderResponse.
        # TODO: Fill in subclassed bot
        :param order_id: Order ID requested to cancel
        :param success: Bool representing if the order was cancelled
        :param error:   Error in cancelling the order (if applicable)
        :return:
        """
        pass

    async def bot_handle_swap_response(self, swap: str, qty: int, success: bool):
        """
        Function for the user to fill in if they want to have any additional actions upon receiving
        a SwapResponse.
        # TODO: Fill in subclassed bot
        :param swap:    Name of the swap
        :param qty:     How many to Swap
        :param success: Swap executed succesfully
        :return:
        """
        pass

    async def bot_handle_news(self, news_release: dict):
        """
        Function for the user to fill in if they want to have any actions upon receiving
        a new release.
        # TODO: Fill in subclassed bot
        :param news:    Dictionary containing data for news.
        :return:
        """
        pass

    async def bot_handle_market_resolved(self, market_id: str, winning_symbol: str, tick: int):
        """Hook for prediction market resolution events."""
        pass

    async def bot_handle_settlement_payout(self, user: str, market_id: str, amount: int, tick: int):
        """Hook for settlement payout events."""
        pass

    def handle_authenticate_response(self, msg):
        if msg.success:
            self.connected = True
            _LOGGER.info("Authenticated by exchange.")
        else:
            _LOGGER.info("The bot was not able to be successfully authenticated. Please validate your credentials.")

    async def process_message(self, msg) -> None:
        """
        Identifies message type and calls the appropriate message handler.
        :param msg: ExchangeMessageToClient
        :return:
        """
        if msg == grpc.aio.EOF:
            _LOGGER.info("End of GRPC stream. Shutting down.")

            # Need to terminate the react process here.

            exit(0)

        msg_type = msg.WhichOneof('body')
        if msg_type is None:
            _LOGGER.debug("Received message with unknown body variant at index %d — proto stubs may need regenerating", msg.index)
            return
        if msg_type not in ("book_snapshot", "book_update", "trade", "cash_update", "position_update"):
            _LOGGER.info("Received message of type %s. index %d", msg_type, msg.index)
        if msg_type == "authenticated":
            self.handle_authenticate_response(msg.authenticated)
        elif msg_type == 'trade':
            await self.handle_trade_msg(msg.trade)
        elif msg_type == 'order_fill':
            await self.handle_order_fill(msg.order_fill)
        elif msg_type == 'order_rejected':
            await self.handle_order_rejected(msg.order_rejected)
        elif msg_type == 'cancel_response':
            await self.handle_cancel_response(msg.cancel_response)
        elif msg_type == 'swap_response':
            await self.handle_swap_response(msg.swap_response)
        elif msg_type == 'book_snapshot':
            await self.handle_book_snapshot(msg.book_snapshot)
        elif msg_type == 'book_update':
            await self.handle_book_update(msg.book_update)
        elif msg_type == 'position_snapshot':
            self.handle_position_snapshot(msg.position_snapshot)
        elif msg_type == 'news_event':
            await self.handle_news_message(msg.news_event)
        elif msg_type == 'market_resolved':
            await self.bot_handle_market_resolved(
                msg.market_resolved.market_id,
                msg.market_resolved.winning_symbol,
                msg.market_resolved.tick,
            )
        elif msg_type == 'settlement_payout':
            await self.bot_handle_settlement_payout(
                msg.settlement_payout.user,
                msg.settlement_payout.market_id,
                msg.settlement_payout.amount,
                msg.settlement_payout.tick,
            )
        elif msg_type == 'cash_update':
            self.positions['cash'] = msg.cash_update.value
        elif msg_type == 'position_update':
            self._ensure_symbol(msg.position_update.symbol)
            self.positions[msg.position_update.symbol] = msg.position_update.value
        elif msg_type == 'error':
            _LOGGER.error(msg.error)
        return
