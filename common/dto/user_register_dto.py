from dataclasses import dataclass
from typing import Optional


@dataclass
class UserRegisterDTO:
    name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    sex: Optional[str] = None
    id_number: Optional[str] = None
    avatar: Optional[str] = None
