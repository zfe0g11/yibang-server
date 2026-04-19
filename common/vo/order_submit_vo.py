from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class OrderSubmitVO:
    id: Optional[int] = None
    order_number: Optional[str] = None
    order_amount: Optional[float] = None
    order_time: Optional[datetime] = None