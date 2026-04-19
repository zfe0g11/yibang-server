from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Dish:
    id: Optional[int] = None
    name: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = None
    image: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    create_user: Optional[int] = None
    update_user: Optional[int] = None