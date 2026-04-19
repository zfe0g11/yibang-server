from dataclasses import dataclass
from typing import Optional


@dataclass
class OrderDetail:
    id: Optional[int] = None
    name: Optional[str] = None
    order_id: Optional[int] = None
    dish_id: Optional[int] = None
    setmeal_id: Optional[int] = None
    dish_flavor: Optional[str] = None
    number: Optional[int] = None
    amount: Optional[float] = None
    image: Optional[str] = None