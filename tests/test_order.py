import pytest
from orderbook.order import Order, OrderType, BidOrAsk, Exchange

def test_order_generation():
    # Test that an order is created with a price and quantity
    order = Order(timestamp = 1625651654, 
                  price = 100.5, 
                  order_id = "abc123", 
                  order_type= OrderType.LIMIT, 
                  quantity = 10, 
                  bid_or_ask=BidOrAsk.BID, 
                  exchange = Exchange.BINANCE)
    assert order.price == 100.5
    assert order.quantity == 10


def test_limit_without_price():
    # Test that an order is created with a price and quantity
    with pytest.raises(ValueError) as e:
        order = Order(timestamp = 1625651654, 
                    order_id = "abc123", 
                    order_type= OrderType.LIMIT, 
                    quantity = 10, 
                    bid_or_ask=BidOrAsk.BID, 
                    exchange = Exchange.BINANCE)
        assert e.message == "Limit orders require a price"