from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

class OrderType(Enum):
    LIMIT = auto()
    MARKET = auto()

class BidOrAsk(Enum):
    BID = auto()
    ASK = auto()

class Exchange(Enum):
    BINANCE = auto()
    LUNO = auto()

class TimeInForce(Enum):
    """Not implemented in this simplified version"""
    GTC = auto()
    IOC = auto()
    FOK = auto()

class OrderStatus(Enum):
    FILLED = auto()
    PARTIALLY_FILLED = auto()
    CANCELLED = auto()
    ERROR = auto()

# convert to Decimals
@dataclass
class Order:
    timestamp: int
    order_type: OrderType
    quantity: float # Decimals
    bid_or_ask: BidOrAsk
    exchange: Exchange
    symbol: Optional[str] = None
    price: Optional[float] = None # Decimals
    order_id: Optional[str] = None
    tif: Optional[TimeInForce] = None # Time in Force (GTC, IOC, FOK)
    order_status: Optional[str] = None

    def __post_init__(self):
        if self.order_type == OrderType.LIMIT and self.price is None:
            raise ValueError("Limit orders require a price")
@dataclass
class Fill:
    """Not implemented in this simplified version"""
    order_id: str
    fill_id: str
    fill_time: float
    fill_price: float
    fill_size: float
    

@dataclass
class Trade:
    """Not implemented in this simplified version"""
    order: Order
    fill: Fill