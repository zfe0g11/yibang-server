from dataclasses import dataclass
from typing import Optional


@dataclass
class DishOverViewVO:
    sold: Optional[int] = None
    discontinued: Optional[int] = None