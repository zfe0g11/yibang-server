from dataclasses import dataclass
from typing import Optional


@dataclass
class PasswordEditDTO:
    emp_id: Optional[int] = None
    old_password: Optional[str] = None
    new_password: Optional[str] = None