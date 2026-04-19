from dataclasses import dataclass
from typing import Optional


@dataclass
class AddressBook:
    id: Optional[int] = None
    user_id: Optional[int] = None
    consignee: Optional[str] = None
    phone: Optional[str] = None
    sex: Optional[str] = None
    province_code: Optional[str] = None
    province_name: Optional[str] = None
    city_code: Optional[str] = None
    city_name: Optional[str] = None
    district_code: Optional[str] = None
    district_name: Optional[str] = None
    detail: Optional[str] = None
    label: Optional[str] = None
    is_default: Optional[int] = None