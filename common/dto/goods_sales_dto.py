from dataclasses import dataclass
from typing import Optional


@dataclass
class GoodsSalesDTO:
    name: Optional[str] = None
    number: Optional[int] = None