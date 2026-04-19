from dataclasses import dataclass
from typing import Optional


@dataclass
class CategoryDTO:
    id: Optional[int] = None
    type: Optional[int] = None
    name: Optional[str] = None
    sort: Optional[int] = None