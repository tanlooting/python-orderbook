from enum import Enum, auto
from dataclasses import dataclass

class OrderType(Enum):
    LIMIT = auto()
    MARKET = auto()

class BidOrAsk(Enum):
    BID = auto()
    ASK = auto()

class Exchange(Enum):
    BINANCE = auto()
    LUNO = auto()
# convert to Decimals
@dataclass
class Order:
    timestamp: int
    order_type: OrderType
    quantity: float # Decimals
    bid_or_ask: BidOrAsk
    exchange: Exchange
    price: float = None # Decimals
    order_id: str = None

    def __post_init__(self):
        if self.order_type == OrderType.LIMIT and self.price is None:
            raise ValueError("Limit orders require a price")
