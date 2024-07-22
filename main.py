from orderbook.order import Order, OrderType, BidOrAsk, Exchange
from orderbook.orderbook import OrderBook

if __name__ == "__main__":
    order_book = OrderBook()
    orders = []
    orders.append(Order(timestamp = 1625651654, 
                  price = 100, 
                  order_id = "a1", 
                  order_type= OrderType.LIMIT, 
                  quantity = 10, 
                  bid_or_ask=BidOrAsk.ASK, 
                  exchange = Exchange.BINANCE))
    orders.append(Order(timestamp = 1625651654, 
                  price = 101, 
                  order_id = "a2", 
                  order_type= OrderType.LIMIT, 
                  quantity = 5, 
                  bid_or_ask=BidOrAsk.ASK, 
                  exchange = Exchange.BINANCE))
    orders.append(Order(timestamp = 1625651654, 
                  price = 101, 
                  order_id = "a3", 
                  order_type= OrderType.LIMIT, 
                  quantity = 10, 
                  bid_or_ask=BidOrAsk.ASK, 
                  exchange = Exchange.BINANCE))
    orders.append(Order(timestamp = 1625651654, 
                  price = 99, 
                  order_id = "b1", 
                  order_type= OrderType.LIMIT, 
                  quantity = 2, 
                  bid_or_ask=BidOrAsk.BID, 
                  exchange = Exchange.BINANCE))
    orders.append(Order(timestamp = 1625651654, 
                  price = 98, 
                  order_id = "b2", 
                  order_type= OrderType.LIMIT, 
                  quantity = 5, 
                  bid_or_ask=BidOrAsk.BID, 
                  exchange = Exchange.BINANCE))
    orders.append(Order(timestamp = 1625651654, 
                  price = 97, 
                  order_id = "b3", 
                  order_type= OrderType.LIMIT, 
                  quantity = 10, 
                  bid_or_ask=BidOrAsk.BID, 
                  exchange = Exchange.BINANCE))

    for o in orders:
        order_book.add_order(o)
    
    order_book.get_L2_orderbook()