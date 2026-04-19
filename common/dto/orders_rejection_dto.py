from dataclasses import dataclass
from typing import Optional


@dataclass
class OrdersRejectionDTO:
    id: Optional[int] = None
    rejection_reason: Optional[str] = None