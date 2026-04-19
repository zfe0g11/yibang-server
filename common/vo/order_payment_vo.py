from dataclasses import dataclass
from typing import Optional


@dataclass
class OrderPaymentVO:
    nonce_str: Optional[str] = None
    pay_sign: Optional[str] = None
    time_stamp: Optional[str] = None
    sign_type: Optional[str] = None
    package_str: Optional[str] = None