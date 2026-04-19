from dataclasses import dataclass
from typing import Optional


@dataclass
class OrderReportVO:
    date_list: Optional[str] = None
    order_count_list: Optional[str] = None
    valid_order_count_list: Optional[str] = None
    total_order_count: Optional[int] = None
    valid_order_count: Optional[int] = None
    order_completion_rate: Optional[float] = None