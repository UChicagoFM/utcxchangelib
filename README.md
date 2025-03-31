
# UChicago Trading xchange-v3-client

## Installation
To get started, pip install the exchange library:
```shell
$ pip install utcxchangelib
```

## Setup
To use the client, create a subclass of the XChangeClient object.

```python
class MyXchangeClient(xchange_client.XChangeClient):
    '''A shell client with the methods that can be implemented to interact with the xchange.'''

     def __init__(self, host: str, username: str, password: str):
        super().__init__(host, username, password)

    async def start(self, user_interface):
        asyncio.create_task(self.trade())

        # This is where Phoenixhood will be launched if desired. There is no need to change these
        # lines, you can either remove the if or delete the whole thing depending on your purposes.
        if user_interface:
            self.launch_user_interface()
            asyncio.create_task(self.handle_queued_messages())

        await self.connect()
```
You should also implement the bot handler methods that are defined. In your bots, you can choose to trade or cancel orders based on the messages received.

```python
class MyXchangeClient(xchange_client.XChangeClient):
     ...
    async def bot_handle_cancel_response(self, order_id: str, success: bool, error: Optional[str]) -> None:
        order = self.open_orders[order_id]
        print(f"{'Market' if order[2] else 'Limit'} Order ID {order_id} cancelled, {order[1]} unfilled")

    async def bot_handle_order_fill(self, order_id: str, qty: int, price: int):
        print("order fill", self.positions)

    async def bot_handle_order_rejected(self, order_id: str, reason: str) -> None:
        print("order rejected because of ", reason)

    async def bot_handle_trade_msg(self, symbol: str, price: int, qty: int):
        pass

    async def bot_handle_book_update(self, symbol: str) -> None:
        pass

    async def bot_handle_swap_response(self, swap: str, qty: int, success: bool):
        pass

    async def bot_handle_news(self, news_release: dict):
        # Parsing the message based on what type was received
        timestamp = news_release["timestamp"] # This is in exchange ticks not ISO or Epoch
        news_type = news_release['kind']
        news_data = news_release["new_data"]

        if news_type == "structured":
            subtype = news_data["structured_subtype"]
            symb = news_data["asset"]
            if subtype == "earnings":
                earnings = news_data["value"]
                ### Do something with this data ###
            else:
                new_signatures = news_data["new_signatures"]
                cumulative = news_data["cumulative"]
                ### Do something with this data ###
        else:
            ### Not sure what you would do with unstructured data.... ###
            pass
```

The next step is to connect your bot to the exchange. To do this, instantiate your bot and call the start function. Now, the bot will connect to the xchange and your bot handlers will be run whenever a message is received from the xchange.

```python
async def main():
    SERVER = 'SERVER URL'
    my_client = MyXchangeClient(SERVER,"USERNAME","PASSWORD")
    await my_client.start()
    return

if __name__ == "__main__":
	...
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(main(user_interface))
```

Your bot can also choose to operate independent of function callbacks from the xchange. To do this, you can use asyncio.create_task to create a task before you start your bot. For example, we created a function below that prints the order books every 3 seconds.

```python
async def view_books(self):
    while True:
        await asyncio.sleep(3)
        for security, book in self.order_books.items():
            sorted_bids = sorted((k,v) for k,v in book.bids.items() if v != 0)
            sorted_asks = sorted((k,v) for k,v in book.asks.items() if v != 0)
            print(f"Bids for {security}:\n{sorted_bids}")
            print(f"Asks for {security}:\n{sorted_asks}")
```

We also need to modify our  **start(self)**  function to create the tasks.

```python
async def start(self, user_interface):
    asyncio.create_task(self.trade())

    # This is where Phoenixhood will be launched if desired. There is no need to change these
    # lines, you can either remove the if or delete the whole thing depending on your purposes.
    if user_interface:
        self.launch_user_interface()
        asyncio.create_task(self.handle_queued_messages())

    await self.connect()
```

The **XChangeClient** that we subclass also has a number of helpful methods implemented to interact with the xchange. You can place and cancel orders, view your positions, view the order books, and place swaps.

```python
async def trade(self):
    """    
    Examples of various XChangeClient actions (limit orders, order cancel, swaps, and market orders)
    """
    # Pause for 5 seconds before starting the trading sequence
    await asyncio.sleep(5)
    print("attempting to trade")

    # Place a BUY limit order for 3 units of APT at price 5
    await self.place_order("APT", 3, xchange_client.Side.BUY, 5)

    # Place a SELL limit order for 3 units of APT at price 7
    await self.place_order("APT", 3, xchange_client.Side.SELL, 7)

    # Pause for 5 seconds to allow orders to be processed
    await asyncio.sleep(5)

    # Cancel the first open order by retrieving its ID from open_orders
    if self.open_orders:
        await self.cancel_order(list(self.open_orders.keys())[0])

    # Place a swap order to swap 1 unit to AKAV
    await self.place_swap_order('toAKAV', 1)

    # Pause for 5 seconds to allow swap to process
    await asyncio.sleep(5)

    # Place a swap order to swap 1 unit from AKAV
    await self.place_swap_order('fromAKAV', 1)

    # Pause for 5 seconds after the swap
    await asyncio.sleep(5)

    # Place a large SELL limit order of 1000 units of APT at price 7
    await self.place_order("APT", 1000, xchange_client.Side.SELL, 7)

    # Pause for 5 seconds before placing a market order
    await asyncio.sleep(5)

    # Place a SELL market order for 10 units of APT
    # Market orders do not have a price, so the price parameter is omitted
    market_order_id = await self.place_order("APT", 10, xchange_client.Side.SELL)

    # Print the ID of the market order for reference
    print("MARKET ORDER ID:", market_order_id)

    # Pause for 5 seconds to allow order to settle
    await asyncio.sleep(5)

    # Print the current positions held after the sequence of trades
    print("my positions:", self.positions)
```

The order books are stored in XChangeClient.order_books. Below is an example code block that prints the sorted order books.

```python
for security, book in self.order_books.items():
    sorted_bids = sorted((k,v) for k,v in book.bids.items() if v != 0)
    sorted_asks = sorted((k,v) for k,v in book.asks.items() if v != 0)
    print(f"Bids for {security}:\n{sorted_bids}")
    print(f"Asks for {security}:\n{sorted_asks}")
```

The positions can be viewed using  `XChangeClient.positions`. Below is an example code block that prints out a user’s positions. The positions are maintained by the bot and are stored in a dictionary.

```python
print("My positions:", self.positions)
```
