# UChicago Trading xchange Client Library

## Installation

```shell
pip install git+https://github.com/UChicagoFM/utcxchangelib.git
```

Requires Python 3.12.

## Setup

Create a subclass of `XChangeClient` and implement the handler methods you care about:

```python
from utcxchangelib import XChangeClient, Side
from typing import Optional
import asyncio


class MyXchangeClient(XChangeClient):

    def __init__(self, host: str, username: str, password: str):
        super().__init__(host, username, password)

    async def bot_handle_cancel_response(self, order_id: str, success: bool, error: Optional[str]) -> None:
        order = self.open_orders[order_id]
        print(f"{'Market' if order[2] else 'Limit'} Order ID {order_id} cancelled, {order[1]} unfilled")

    async def bot_handle_order_fill(self, order_id: str, qty: int, price: int):
        print("order fill", self.positions)

    async def bot_handle_order_rejected(self, order_id: str, reason: str) -> None:
        print("order rejected because of", reason)

    async def bot_handle_trade_msg(self, symbol: str, price: int, qty: int):
        pass

    async def bot_handle_book_update(self, symbol: str) -> None:
        pass

    async def bot_handle_swap_response(self, swap: str, qty: int, success: bool):
        pass

    async def bot_handle_news(self, news_release: dict):
        tick = news_release["tick"]
        news_type = news_release["kind"]
        symbol = news_release["symbol"]  # may be None
        news_data = news_release["new_data"]

        if news_type == "structured":
            subtype = news_data["structured_subtype"]
            if subtype == "earnings":
                asset = news_data["asset"]
                value = news_data["value"]
            elif subtype == "cpi_print":
                forecast = news_data["forecast"]
                actual = news_data["actual"]
        else:
            content = news_data["content"]
            message_type = news_data["type"]

    async def bot_handle_market_resolved(self, market_id: str, winning_symbol: str, tick: int):
        print(f"Market {market_id} resolved: winner is {winning_symbol}")

    async def bot_handle_settlement_payout(self, user: str, market_id: str, amount: int, tick: int):
        print(f"Settlement payout: {amount} from {market_id}")

    async def trade(self):
        await asyncio.sleep(5)
        # Your trading logic here

    async def start(self):
        asyncio.create_task(self.trade())
        await self.connect()
```

Connect to the exchange:

```python
async def main():
    SERVER = "SERVER_HOST:3333"
    my_client = MyXchangeClient(SERVER, "USERNAME", "PASSWORD")
    await my_client.start()


if __name__ == "__main__":
    asyncio.run(main())
```

## Placing Orders

```python
async def trade(self):
    await asyncio.sleep(5)

    # Limit order: BUY 3 units of A at price 5
    await self.place_order("A", 3, Side.BUY, 5)

    # Limit order: SELL 3 units of A at price 7
    await self.place_order("A", 3, Side.SELL, 7)

    await asyncio.sleep(5)

    # Cancel the first open order
    if self.open_orders:
        await self.cancel_order(list(self.open_orders.keys())[0])

    # Market order: SELL 10 units of B (no price = market order)
    market_order_id = await self.place_order("B", 10, Side.SELL)
    print("Market order ID:", market_order_id)
```

## Swaps

Create an ETF from its components (A + B + C -> ETF), or redeem:

```python
# Create 1 ETF (costs 5 cash, consumes 1 each of A, B, C)
await self.place_swap_order("toETF", 1)

# Redeem 1 ETF (costs 5 cash, produces 1 each of A, B, C)
await self.place_swap_order("fromETF", 1)
```

## Order Books

```python
for symbol, book in self.order_books.items():
    sorted_bids = sorted((k, v) for k, v in book.bids.items() if v != 0)
    sorted_asks = sorted((k, v) for k, v in book.asks.items() if v != 0)
    print(f"Bids for {symbol}: {sorted_bids}")
    print(f"Asks for {symbol}: {sorted_asks}")
```

## Positions

```python
print("My positions:", self.positions)
```

## Symbols

The default symbols are:

| Symbol | Description |
|--------|-------------|
| A, B, C | Equities |
| ETF | Weighted basket of A + B + C |
| B_C_950, B_P_950, B_C_1000, B_P_1000, B_C_1050, B_P_1050 | Options on B (calls and puts) |
| R_CUT, R_HOLD, R_HIKE | Prediction market contracts (Fed decision) |

You can also pass custom `symbols` and `swap_map` to the constructor if needed:

```python
client = XChangeClient(host, username, password, symbols=["A", "B", "C"])
```
