from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class DishVO:
    id: Optional[int] = None
    name: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = None
    image: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None
    update_time: Optional[datetime] = None
    category_name: Optional[str] = None
    flavors: Optional[List[any]] = None