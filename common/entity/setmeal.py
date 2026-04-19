from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Setmeal:
    id: Optional[int] = None
    category_id: Optional[int] = None
    name: Optional[str] = None
    price: Optional[float] = None
    status: Optional[int] = None
    description: Optional[str] = None
    image: Optional[str] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    create_user: Optional[int] = None
    update_user: Optional[int] = None