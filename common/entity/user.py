from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: Optional[int] = None
    openid: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    sex: Optional[str] = None
    id_number: Optional[str] = None
    avatar: Optional[str] = None
    create_time: Optional[datetime] = None