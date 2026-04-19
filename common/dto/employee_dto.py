from dataclasses import dataclass
from typing import Optional


@dataclass
class EmployeeDTO:
    id: Optional[int] = None
    username: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    sex: Optional[str] = None
    id_number: Optional[str] = None