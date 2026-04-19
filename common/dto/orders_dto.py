from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class OrdersDTO:
    id: Optional[int] = None
    number: Optional[str] = None
    status: Optional[int] = None
    user_id: Optional[int] = None
    address_book_id: Optional[int] = None
    order_time: Optional[datetime] = None
    checkout_time: Optional[datetime] = None
    pay_method: Optional[int] = None
    amount: Optional[float] = None
    remark: Optional[str] = None
    user_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None