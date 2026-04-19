from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ShoppingCart:
    id: Optional[int] = None
    name: Optional[str] = None
    user_id: Optional[int] = None
    dish_id: Optional[int] = None
    setmeal_id: Optional[int] = None
    dish_flavor: Optional[str] = None
    number: Optional[int] = None
    amount: Optional[float] = None
    image: Optional[str] = None
    create_time: Optional[datetime] = None