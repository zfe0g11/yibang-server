from dataclasses import dataclass
from typing import Optional


@dataclass
class DishItemVO:
    name: Optional[str] = None
    copies: Optional[int] = None
    image: Optional[str] = None
    description: Optional[str] = None