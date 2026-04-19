from dataclasses import dataclass
from typing import Optional


@dataclass
class EmployeeLoginDTO:
    username: Optional[str] = None
    password: Optional[str] = None