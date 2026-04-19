from dataclasses import dataclass
from typing import Optional


@dataclass
class OrdersPaymentDTO:
    order_number: Optional[str] = None
    pay_method: Optional[int] = None