from dataclasses import dataclass
from typing import Optional


@dataclass
class OrderOverViewVO:
    waiting_orders: Optional[int] = None
    delivered_orders: Optional[int] = None
    completed_orders: Optional[int] = None
    cancelled_orders: Optional[int] = None
    all_orders: Optional[int] = None