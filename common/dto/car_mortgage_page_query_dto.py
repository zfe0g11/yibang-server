from dataclasses import dataclass
from typing import Optional


@dataclass
class CarMortgagePageQueryDTO:
    car_name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    status: Optional[int] = None
    page: int = 1
    page_size: int = 10
