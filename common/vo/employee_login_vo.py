from dataclasses import dataclass
from typing import Optional


@dataclass
class EmployeeLoginVO:
    id: Optional[int] = None
    user_name: Optional[str] = None
    name: Optional[str] = None
    token: Optional[str] = None