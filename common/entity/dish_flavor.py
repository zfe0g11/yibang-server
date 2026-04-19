from dataclasses import dataclass
from typing import Optional


@dataclass
class DishFlavor:
    id: Optional[int] = None
    dish_id: Optional[int] = None
    name: Optional[str] = None
    value: Optional[str] = None