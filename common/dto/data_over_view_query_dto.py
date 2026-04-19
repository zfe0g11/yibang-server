from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class DataOverViewQueryDTO:
    begin: Optional[datetime] = None
    end: Optional[datetime] = None