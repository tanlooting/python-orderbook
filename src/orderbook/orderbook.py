from collections import deque
from typing import Deque, Dict, Optional, Any
from orderbook.order import Order, OrderType, BidOrAsk
from sortedcontainers import SortedDict
from termcolor import cprint

class OrderBook:
    def __init__(self):
        self.bids: SortedDict[float, Deque] = SortedDict() 
        self.asks: SortedDict[float, Deque] = SortedDict()
        self.id_to_price: Dict[str, float] = dict() # for ease of finding price
        self.pending_market_orders_bid: Deque[Order] = deque()
        self.pending_market_orders_ask: Deque[Order] = deque()
        self.trades = list() # unused

    def process_order(self, order: Order):
        if order.order_type == OrderType.LIMIT:
            self.process_limit_order(order)
        elif order.order_type == OrderType.MARKET:
            self.process_market_order(order)

    def process_limit_order(self, order: Order):
        quantity_remaining = order.quantity

        if order.bid_or_ask == BidOrAsk.BID:
            if self.asks and order.price >= self.get_best_ask():
                # crossing spread
                while self.get_best_ask() <= order.price:
                    price = self.get_best_ask()
                    order_deque = self.asks[price]
                    while order_deque:
                        o = order_deque[0]
                        if quantity_remaining > o.quantity:
                            quantity_remaining -= o.quantity
                            self.id_to_price.pop(o.order_id)
                            order_deque.popleft()
                        elif quantity_remaining <= o.quantity:
                            o.quantity -= quantity_remaining
                            quantity_remaining = 0

                        if quantity_remaining == 0:
                            break
                    if len(self.asks[price]) == 0:
                        self.asks.pop(price)
                    if quantity_remaining == 0: break
                    
                # if remaining, the rest gets added to the book and sit as limit.
                if quantity_remaining > 0:
                    order.quantity = quantity_remaining
                    self.add_order(order)
            else:
                self.add_order(order)

        elif order.bid_or_ask == BidOrAsk.ASK:
            if self.bids and order.price <= self.get_best_bid():
                # crossing spread
                while self.get_best_bid() >= order.price:
                    price = self.get_best_bid()
                    order_deque = self.bids[price]
                    while order_deque:
                        o = order_deque[0]
                        if quantity_remaining > o.quantity:
                            quantity_remaining -= o.quantity
                            self.id_to_price.pop(o.order_id)
                            order_deque.popleft()
                        elif quantity_remaining <= o.quantity:
                            o.quantity -= quantity_remaining
                            quantity_remaining = 0

                        if quantity_remaining == 0: break
                    if len(self.bids[price]) == 0:
                        self.bids.pop(price)
                    if quantity_remaining == 0: break
                # if remaining, the rest gets added to the book and sit as limit.
                if quantity_remaining > 0:
                    order.quantity = quantity_remaining
                    self.add_order(order)
            else:
                self.add_order(order)
        else: # if orderbook completely empty
            self.add_order(order)

    def process_market_order(self, order: Order):

        quantity_remaining = order.quantity 
        # match against other market orders if no limit orders available
        if order.bid_or_ask == BidOrAsk.BID and not self.asks:
            while self.pending_market_orders_ask:
                o = self.pending_market_orders_ask[0]
                if quantity_remaining > o.quantity:
                    quantity_remaining -= o.quantity
                    self.pending_market_orders_ask.popleft()
                elif quantity_remaining <= o.quantity:
                    o.quantity -= quantity_remaining
                    quantity_remaining = 0
                    break
        elif order.bid_or_ask == BidOrAsk.ASK and not self.bids:
            while self.pending_market_orders_bid:
                o = self.pending_market_orders_bid[0]
                if quantity_remaining > o.quantity:
                    quantity_remaining -= o.quantity
                    self.pending_market_orders_bid.popleft()
                elif quantity_remaining <= o.quantity:
                    o.quantity -= quantity_remaining
                    quantity_remaining = 0
                    break

        # if can match to limit orders
        if order.bid_or_ask == BidOrAsk.BID:
            while quantity_remaining > 0 and self.asks:
                price = self.get_best_ask()
                order_deque = self.asks[price]
                
                while order_deque:
                    o = order_deque[0]
                    if quantity_remaining > o.quantity:
                        quantity_remaining -= o.quantity
                        self.id_to_price.pop(o.order_id)
                        order_deque.popleft()
                    elif quantity_remaining <= o.quantity:
                        o.quantity -= quantity_remaining
                        quantity_remaining = 0
                        break
                if len(self.asks[price]) == 0:
                    self.asks.pop(price)
                

        elif order.bid_or_ask == BidOrAsk.ASK:
            while quantity_remaining > 0 and self.bids:
                price = self.get_best_bid()
                order_deque = self.bids[price]
                
                while order_deque:
                    o = order_deque[0]
                    if quantity_remaining > o.quantity:
                        quantity_remaining -= o.quantity
                        self.id_to_price.pop(o.order_id)
                        order_deque.popleft()
                    elif quantity_remaining <= o.quantity:
                        o.quantity -= quantity_remaining
                        quantity_remaining = 0
                        break
                if len(self.bids[price]) == 0:
                    self.bids.pop(price)
        
        # if market orders are not fully filled, add it to pending_market_orders
        # next limit order that gets added will fulfill the remaining market orders
        if quantity_remaining > 0:
            order.quantity = quantity_remaining
            if order.bid_or_ask == BidOrAsk.BID:
                self.pending_market_orders_bid.append(order)
            elif order.bid_or_ask == BidOrAsk.ASK:
                self.pending_market_orders_ask.append(order)


    def cancel_order(self, order_id: str):
        price = self.id_to_price[order_id]
        self.id_to_price.pop(order_id)
        if price in self.bids:
            for o in self.bids[price]:
                if o.order_id == order_id:
                    self.bids[price].remove(o)
                    break
            if len(self.bids[price]) == 0:
                self.bids.pop(price)

        elif price in self.asks:
            for o in self.asks[price]:
                if o.order_id == order_id:
                    self.asks[price].remove(o)
                    
                    break
            if len(self.asks[price]) == 0:
                self.asks.pop(price)
                    

    def add_order(self, order: Order):
        self.id_to_price[order.order_id] = order.price
        if order.bid_or_ask == BidOrAsk.BID:
            if self.bids.get(order.price) is not None:
                self.bids[order.price].append(order)
            else:
                self.bids[order.price] = deque([order])
        if order.bid_or_ask == BidOrAsk.ASK:
            if self.asks.get(order.price) is not None:
                self.asks[order.price].append(order)
            else:
                self.asks[order.price] = deque([order])
        
        # once added order, check if there are any pending market orders
        if order.bid_or_ask == BidOrAsk.BID and self.pending_market_orders_ask:
            market_order = self.pending_market_orders_ask.popleft()
            self.process_order(market_order)
        elif order.bid_or_ask == BidOrAsk.ASK and self.pending_market_orders_bid:
            market_order = self.pending_market_orders_bid.popleft()
            self.process_order(market_order)
        
            
    
    def get_best_bid(self) -> Any:
        return self.bids.peekitem()[0]
    
    def get_best_ask(self) -> Any:
        return self.asks.peekitem(0)[0]
    
    def get_L2_orderbook(self, 
                         disp_levels: Optional[int] = None):
        """print aggregated orderbook to console
        price-> quantity
        """
        self.agg_asks = SortedDict()
        self.agg_bids = SortedDict()
        for price, order_deque in self.asks.items():
            self.agg_asks[price] = sum([o.quantity for o in order_deque])
        for price, order_deque in self.bids.items():
            self.agg_bids[price] = sum([o.quantity for o in order_deque])
        
        
        cprint("-------ASKS-------\n", "red", attrs = ["bold"])
        for k in reversed(self.agg_asks.keys()):
            print(f"Price: {k}, Quantity: {self.agg_asks[k]}\n")
        cprint("-------BIDS-------\n", "green", attrs = ["bold"])
        for k in reversed(self.agg_bids.keys()):
            print(f"Price: {k}, Quantity: {self.agg_bids[k]}\n")

        