from dataclasses import dataclass
from typing import Optional


@dataclass
class UserLoginDTO:
    phone: Optional[str] = None
    password: Optional[str] = None