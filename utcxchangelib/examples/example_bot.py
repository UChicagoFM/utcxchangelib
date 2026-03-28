from typing import Optional

from utcxchangelib import XChangeClient, Side
import asyncio


class MyXchangeClient(XChangeClient):

    def __init__(self, host: str, username: str, password: str):
        super().__init__(host, username, password)

    async def bot_handle_cancel_response(self, order_id: str, success: bool, error: Optional[str] = None) -> None:
        pass

    async def bot_handle_order_fill(self, order_id: str, qty: int, price: int):
        pass

    async def bot_handle_order_rejected(self, order_id: str, reason: str) -> None:
        pass

    async def bot_handle_trade_msg(self, symbol: str, price: int, qty: int):
        pass

    async def bot_handle_book_update(self, symbol: str) -> None:
        pass

    async def bot_handle_swap_response(self, swap: str, qty: int, success: bool):
        pass

    async def trade(self):
        """This is a simple example bot that places orders and prints updates."""
        await asyncio.sleep(5)

        # Place an order
        await self.place_order("A", 10, Side.BUY, 100)

        # You can also look at order books like this
        for security, book in self.order_books.items():
            if book.bids or book.asks:
                sorted_bids = sorted((k,v) for k,v in book.bids.items() if v != 0)
                sorted_asks = sorted((k,v) for k,v in book.asks.items() if v != 0)
                print(f"Bids for {security}:\n{sorted_bids}")
                print(f"Asks for {security}:\n{sorted_asks}")

    async def start(self):
        asyncio.create_task(self.trade())
        await self.connect()


async def main():
    SERVER = '127.0.0.1:3333'
    my_client = MyXchangeClient(SERVER, "user", "password")
    await my_client.start()


if __name__ == "__main__":
    asyncio.run(main())
