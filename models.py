from enum import Enum
from typing import Dict
from uuid import uuid4

class Role(str, Enum):
    passenger = "passenger"
    admin = "admin"

class BookingStatus(str, Enum):
    draft = "draft"
    paid = "paid"
    checked_in = "checked_in"
    cancelled = "cancelled"

class PaymentStatus(str, Enum):
    pending = "pending"
    success = "success"
    failed = "failed"

DB: Dict[str, Dict[str, Dict]] = {
    "users": {},
    "airports": {},
    "flights": {},
    "bookings": {},
    "payments": {},
}

def generate_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8]}"
