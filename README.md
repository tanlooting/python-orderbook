# Orderbook & Matching Engine in Python

This repo implements an orderbook on python using the Sorted Containers library and Deque.

Each bid and ask trees is represented by a sortedDict with price keys and Order list in a deque. 

Deque contains the list of Order objects defined in `order.py`.

At this moment, it only handles `limit` and `market` order types.

## Getting Started
```
orderbook = Orderbook()

o = Order(
        timestamp = 1625651654, 
        price = 99, 
        order_id = "b1", 
        order_type= OrderType.LIMIT, 
        quantity = 2, 
        bid_or_ask=BidOrAsk.BID, 
        exchange = Exchange.BINANCE
        )
orderbook.process_order(o)

```

## Todo:
- modify orders (allowing modification of limit order quantity)
- Adding fill objects into trade objects
  - Trade object should contain order information, and fill information

## Reference:
https://grantjenks.com/docs/sortedcontainers/ 