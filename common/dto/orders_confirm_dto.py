from dataclasses import dataclass
from typing import Optional


@dataclass
class OrdersConfirmDTO:
    id: Optional[int] = None
    status: Optional[int] = None