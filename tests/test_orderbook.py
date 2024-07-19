import pytest
from src.orderbook.order import Order, OrderType, BidOrAsk, Exchange
from src.orderbook.orderbook import OrderBook

def test_add_order_new_price():
    """add a new limit order with a new price"""
    order_book = OrderBook()
    order = Order(timestamp = 1625651654, 
                  price = 100.5, 
                  order_id = "abc123", 
                  order_type= OrderType.LIMIT, 
                  quantity = 10, 
                  bid_or_ask=BidOrAsk.BID, 
                  exchange = Exchange.BINANCE)
    order_book.add_order(order)
    print(order_book.bids[100.5])
    assert len(order_book.bids) == 1
    assert len(order_book.asks) == 0

def test_get_best_bid():
    order_book = OrderBook()
    order_1 = Order(timestamp = 1625651654, 
                  price = 100, 
                  order_id = "b1", 
                  order_type= OrderType.LIMIT, 
                  quantity = 10, 
                  bid_or_ask=BidOrAsk.BID, 
                  exchange = Exchange.BINANCE)
    order_2 = Order(timestamp = 1625651654, 
                  price = 101, 
                  order_id = "b2", 
                  order_type= OrderType.LIMIT, 
                  quantity = 5, 
                  bid_or_ask=BidOrAsk.BID, 
                  exchange = Exchange.BINANCE)
    order_book.add_order(order_1)
    order_book.add_order(order_2)
    assert len(order_book.bids) == 2
    assert order_book.get_best_bid() == 101

def test_get_best_asks():
    order_book = OrderBook()
    order_1 = Order(timestamp = 1625651654, 
                  price = 100, 
                  order_id = "a1", 
                  order_type= OrderType.LIMIT, 
                  quantity = 10, 
                  bid_or_ask=BidOrAsk.ASK, 
                  exchange = Exchange.BINANCE)
    order_2 = Order(timestamp = 1625651654, 
                  price = 101, 
                  order_id = "a2", 
                  order_type= OrderType.LIMIT, 
                  quantity = 5, 
                  bid_or_ask=BidOrAsk.ASK, 
                  exchange = Exchange.BINANCE)
    order_book.add_order(order_1)
    order_book.add_order(order_2)
    assert len(order_book.asks) == 2
    assert order_book.get_best_ask() == 100


def test_cancel_order():
    order_book = OrderBook()
    order_1 = Order(timestamp = 1625651654, 
                  price = 100, 
                  order_id = "a1", 
                  order_type= OrderType.LIMIT, 
                  quantity = 10, 
                  bid_or_ask=BidOrAsk.ASK, 
                  exchange = Exchange.BINANCE)
    order_2 = Order(timestamp = 1625651654, 
                  price = 101, 
                  order_id = "a2", 
                  order_type= OrderType.LIMIT, 
                  quantity = 5, 
                  bid_or_ask=BidOrAsk.ASK, 
                  exchange = Exchange.BINANCE)
    order_book.add_order(order_1)
    order_book.add_order(order_2)
    order_book.cancel_order("a1")
    assert len(order_book.asks) == 1
    assert order_book.get_best_ask() == 101

def test_market_order_complete_fill():
    order_book = OrderBook()
    order_1 = Order(timestamp = 1625651654, 
                  price = 100, 
                  order_id = "a1", 
                  order_type= OrderType.LIMIT, 
                  quantity = 10, 
                  bid_or_ask=BidOrAsk.ASK, 
                  exchange = Exchange.BINANCE)
    order_2 = Order(timestamp = 1625651654, 
                  price = 100, 
                  order_id = "a2", 
                  order_type= OrderType.LIMIT, 
                  quantity = 5, 
                  bid_or_ask=BidOrAsk.ASK, 
                  exchange = Exchange.BINANCE)
    order_3 = Order(timestamp = 1625651654, 
                  price = 101, 
                  order_id = "a3", 
                  order_type= OrderType.LIMIT, 
                  quantity = 10, 
                  bid_or_ask=BidOrAsk.ASK, 
                  exchange = Exchange.BINANCE)
    market_order = Order(timestamp = 1625651654,
                  order_id = "a4", 
                  order_type= OrderType.MARKET, 
                  quantity = 20, 
                  bid_or_ask=BidOrAsk.BID, 
                  exchange = Exchange.BINANCE)
    order_book.add_order(order_1)
    order_book.add_order(order_2)
    order_book.add_order(order_3)
    order_book.process_order(market_order)
    assert len(order_book.asks) == 1
    assert order_book.get_best_ask() == 101
    assert order_book.asks[order_book.get_best_ask()][0].quantity == 5

def test_market_order_partial_fill():
    order_book = OrderBook()
    order_1 = Order(timestamp = 1625651654, 
                  price = 100, 
                  order_id = "a1", 
                  order_type= OrderType.LIMIT, 
                  quantity = 10, 
                  bid_or_ask=BidOrAsk.ASK, 
                  exchange = Exchange.BINANCE)
    order_2 = Order(timestamp = 1625651654, 
                  price = 100, 
                  order_id = "a2", 
                  order_type= OrderType.LIMIT, 
                  quantity = 5, 
                  bid_or_ask=BidOrAsk.ASK, 
                  exchange = Exchange.BINANCE)
    order_3 = Order(timestamp = 1625651654, 
                  price = 101, 
                  order_id = "a3", 
                  order_type= OrderType.LIMIT, 
                  quantity = 10, 
                  bid_or_ask=BidOrAsk.ASK, 
                  exchange = Exchange.BINANCE)
    market_order = Order(timestamp = 1625651654,
                  order_id = "a4", 
                  order_type= OrderType.MARKET, 
                  quantity = 30, 
                  bid_or_ask=BidOrAsk.BID, 
                  exchange = Exchange.BINANCE)
    order_book.add_order(order_1)
    order_book.add_order(order_2)
    order_book.add_order(order_3)
    order_book.process_order(market_order)
    assert len(order_book.asks) == 0
    assert len(order_book.pending_market_orders) == 1
    assert order_book.pending_market_orders[0].quantity == 5
    

def test_market_order_empty_book_and_add_new_limit():
    """
    1. Test market order when the order book is empty
    2. Test if market order is filled when a new limit order is added
    """
    order_book = OrderBook()
    market_order = Order(timestamp = 1625651654,
                  order_id = "a4", 
                  order_type= OrderType.MARKET, 
                  quantity = 30, 
                  bid_or_ask=BidOrAsk.BID, 
                  exchange = Exchange.BINANCE)
    order_book.process_order(market_order)
    assert len(order_book.pending_market_orders) == 1

    # after limit order is added, the market order should continue to be filled
    order_1 = Order(timestamp = 1625651654, 
                  price = 100, 
                  order_id = "a1", 
                  order_type= OrderType.LIMIT, 
                  quantity = 10, 
                  bid_or_ask=BidOrAsk.ASK, 
                  exchange = Exchange.BINANCE)
    order_book.add_order(order_1)
    assert len(order_book.asks) == 0
    assert len(order_book.pending_market_orders) == 1
    assert order_book.pending_market_orders[0].quantity == 20

def test_add_limit_orders():
    """without crossing spread"""
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
    for order in orders:
        order_book.process_order(order)
    
    assert len(order_book.asks) == 2
    assert len(order_book.bids) == 3

def test_cross_spread_bid_limit_partially_filled():
    """partially filled a cross spread limit order
    but not enough of the quantity in the opposite tree
    remaining order should be kept in opposite tree """
    order_book = OrderBook()
    orders = []
    orders.append(Order(timestamp = 1625651654, 
                  price = 100, 
                  order_id = "a1", 
                  order_type= OrderType.LIMIT, 
                  quantity = 5, 
                  bid_or_ask=BidOrAsk.ASK, 
                  exchange = Exchange.BINANCE))
    orders.append(Order(timestamp = 1625651654, 
                  price = 101, 
                  order_id = "a2", 
                  order_type= OrderType.LIMIT, 
                  quantity = 10, 
                  bid_or_ask=BidOrAsk.ASK, 
                  exchange = Exchange.BINANCE))

    orders.append(Order(timestamp = 1625651654, 
                  price = 100, 
                  order_id = "b1", 
                  order_type= OrderType.LIMIT, 
                  quantity = 10, 
                  bid_or_ask=BidOrAsk.BID, 
                  exchange = Exchange.BINANCE)) 
    
    # 5 of b1 will be filled by a1, remaining 5 will sit in bids tree
    for order in orders:
        order_book.process_order(order)
    
    assert order_book.get_best_bid() == 100
    assert order_book.get_best_ask() == 101
    assert order_book.bids[order_book.get_best_bid()][0].quantity == 5


def test_cross_spread_ask_limit_partially_filled():
    """partially filled a cross spread limit order
    but not enough of the quantity in the opposite tree
    remaining order should be kept in opposite tree """
    order_book = OrderBook()
    orders = []
    orders.append(Order(timestamp = 1625651654, 
                  price = 101, 
                  order_id = "b1", 
                  order_type= OrderType.LIMIT, 
                  quantity = 5, 
                  bid_or_ask=BidOrAsk.BID, 
                  exchange = Exchange.BINANCE))
    orders.append(Order(timestamp = 1625651654, 
                  price = 100, 
                  order_id = "b2", 
                  order_type= OrderType.LIMIT, 
                  quantity = 10, 
                  bid_or_ask=BidOrAsk.BID, 
                  exchange = Exchange.BINANCE))

    orders.append(Order(timestamp = 1625651654, 
                  price = 101, 
                  order_id = "a1", 
                  order_type= OrderType.LIMIT, 
                  quantity = 10, 
                  bid_or_ask=BidOrAsk.ASK, 
                  exchange = Exchange.BINANCE)) 
    
    # 5 of b1 will be filled by a1, remaining 5 will sit in bids tree
    for order in orders:
        order_book.process_order(order)
    
    assert order_book.get_best_bid() == 100
    assert order_book.get_best_ask() == 101
    assert order_book.asks[order_book.get_best_ask()][0].quantity == 5

