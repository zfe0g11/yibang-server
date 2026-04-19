from dataclasses import dataclass
from typing import Optional


@dataclass
class SetmealOverViewVO:
    sold: Optional[int] = None
    discontinued: Optional[int] = None