from dataclasses import dataclass
from typing import Optional


@dataclass
class EmployeePageQueryDTO:
    name: Optional[str] = None
    page: int = 1
    page_size: int = 10