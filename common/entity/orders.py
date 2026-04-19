from dataclasses import dataclass
from datetime import datetime
from typing import Optional


class Orders:
    # 订单状态
    PENDING_PAYMENT = 1
    TO_BE_CONFIRMED = 2
    CONFIRMED = 3
    DELIVERY_IN_PROGRESS = 4
    COMPLETED = 5
    CANCELLED = 6
    
    # 支付状态
    UN_PAID = 0
    PAID = 1
    REFUND = 2


@dataclass
class OrdersEntity:
    id: Optional[int] = None
    number: Optional[str] = None
    status: Optional[int] = None
    user_id: Optional[int] = None
    address_book_id: Optional[int] = None
    order_time: Optional[datetime] = None
    checkout_time: Optional[datetime] = None
    pay_method: Optional[int] = None
    pay_status: Optional[int] = None
    amount: Optional[float] = None
    remark: Optional[str] = None
    user_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    consignee: Optional[str] = None
    cancel_reason: Optional[str] = None
    rejection_reason: Optional[str] = None
    cancel_time: Optional[datetime] = None
    estimated_delivery_time: Optional[datetime] = None
    delivery_status: Optional[int] = None
    delivery_time: Optional[datetime] = None