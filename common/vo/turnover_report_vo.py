from dataclasses import dataclass
from typing import Optional


@dataclass
class TurnoverReportVO:
    date_list: Optional[str] = None
    turnover_list: Optional[str] = None