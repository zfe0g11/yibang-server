from dataclasses import dataclass
from typing import Optional


@dataclass
class ShoppingCartDTO:
    dish_id: Optional[int] = None
    setmeal_id: Optional[int] = None
    dish_flavor: Optional[str] = None