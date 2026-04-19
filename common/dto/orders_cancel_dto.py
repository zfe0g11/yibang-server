from dataclasses import dataclass
from typing import Optional


@dataclass
class OrdersCancelDTO:
    id: Optional[int] = None
    cancel_reason: Optional[str] = None