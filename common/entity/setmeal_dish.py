from dataclasses import dataclass
from typing import Optional


@dataclass
class SetmealDish:
    id: Optional[int] = None
    setmeal_id: Optional[int] = None
    dish_id: Optional[int] = None
    name: Optional[str] = None
    price: Optional[float] = None
    copies: Optional[int] = None