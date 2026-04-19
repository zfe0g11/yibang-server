from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class SetmealVO:
    id: Optional[int] = None
    category_id: Optional[int] = None
    name: Optional[str] = None
    price: Optional[float] = None
    status: Optional[int] = None
    description: Optional[str] = None
    image: Optional[str] = None
    update_time: Optional[datetime] = None
    category_name: Optional[str] = None
    setmeal_dishes: Optional[List[any]] = None