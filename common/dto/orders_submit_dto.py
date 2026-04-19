from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class OrdersSubmitDTO:
    address_book_id: Optional[int] = None
    pay_method: Optional[int] = None
    remark: Optional[str] = None
    estimated_delivery_time: Optional[datetime] = None
    delivery_status: Optional[int] = None
    tableware_number: Optional[int] = None
    tableware_status: Optional[int] = None
    pack_amount: Optional[int] = None
    amount: Optional[float] = None