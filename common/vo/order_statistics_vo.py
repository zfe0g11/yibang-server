from dataclasses import dataclass
from typing import Optional


@dataclass
class OrderStatisticsVO:
    to_be_confirmed: Optional[int] = None
    confirmed: Optional[int] = None
    delivery_in_progress: Optional[int] = None