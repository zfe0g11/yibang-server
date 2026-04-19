from dataclasses import dataclass
from typing import Optional, List


@dataclass
class SetmealDTO:
    id: Optional[int] = None
    category_id: Optional[int] = None
    name: Optional[str] = None
    price: Optional[float] = None
    status: Optional[int] = None
    description: Optional[str] = None
    image: Optional[str] = None
    setmeal_dishes: Optional[List[any]] = None