from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Category:
    id: Optional[int] = None
    type: Optional[int] = None
    name: Optional[str] = None
    sort: Optional[int] = None
    status: Optional[int] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    create_user: Optional[int] = None
    update_user: Optional[int] = None