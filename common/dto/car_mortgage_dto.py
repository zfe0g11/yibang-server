from dataclasses import dataclass
from typing import Optional, List

@dataclass
class CarMortgageDTO:
    openid: Optional[str] = None
    car_name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    description: Optional[str] = None
    images: Optional[List[str]] = None