from dataclasses import dataclass
from typing import Optional


@dataclass
class UserLoginVO:
    id: Optional[int] = None
    openid: Optional[str] = None
    token: Optional[str] = None