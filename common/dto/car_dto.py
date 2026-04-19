from dataclasses import dataclass
from typing import Optional, List


@dataclass
class CarDTO:
    id: Optional[int] = None
    name: Optional[str] = None
    model_id: Optional[int] = None
    brand_id : Optional[int] = None
    price: Optional[float] = None
    image: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None