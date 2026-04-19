from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Employee:
    id: Optional[int] = None
    username: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    sex: Optional[str] = None
    id_number: Optional[str] = None
    status: Optional[int] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    create_user: Optional[int] = None
    update_user: Optional[int] = None