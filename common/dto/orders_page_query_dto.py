from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class OrdersPageQueryDTO:
    page: int = 1
    page_size: int = 10
    number: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[int] = None
    begin_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    user_id: Optional[int] = None