from dataclasses import dataclass
from typing import Optional


@dataclass
class DishPageQueryDTO:
    page: int = 1
    page_size: int = 10
    name: Optional[str] = None
    category_id: Optional[int] = None
    status: Optional[int] = None