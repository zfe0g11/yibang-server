from dataclasses import dataclass
from typing import Optional


@dataclass
class CarMortgageAuditDTO:
    id: int
    status: int  # 1-审核通过，2-审核拒绝
