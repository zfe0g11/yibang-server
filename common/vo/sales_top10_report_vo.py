from dataclasses import dataclass
from typing import Optional


@dataclass
class SalesTop10ReportVO:
    name_list: Optional[str] = None
    number_list: Optional[str] = None