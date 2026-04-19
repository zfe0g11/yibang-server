from dataclasses import dataclass
from typing import Optional


@dataclass
class UserReportVO:
    date_list: Optional[str] = None
    total_user_list: Optional[str] = None
    new_user_list: Optional[str] = None