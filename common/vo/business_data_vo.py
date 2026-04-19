from dataclasses import dataclass
from typing import Optional


@dataclass
class BusinessDataVO:
    turnover: Optional[float] = None
    valid_order_count: Optional[int] = None
    order_completion_rate: Optional[float] = None
    unit_price: Optional[float] = None
    new_users: Optional[int] = None