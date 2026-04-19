from dataclasses import dataclass
from typing import Optional


@dataclass
class CategoryPageQueryDTO:
    page: int = 1
    page_size: int = 10
    name: Optional[str] = None
    type: Optional[int] = None