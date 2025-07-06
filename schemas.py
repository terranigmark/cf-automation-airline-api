from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, constr
from models import Role, BookingStatus, PaymentStatus

# Common type for IATA codes
IATACode = constr(pattern=r"^[A-Z]{3}$")

# ---------- AUTH ----------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ---------- USERS ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: str

class UserCreateAdmin(UserCreate):
    role: Role

class UserOut(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    role: Role

# ---------- AIRPORTS ----------
class AirportCreate(BaseModel):
    iata_code: IATACode
    city: str
    country: str

class AirportOut(AirportCreate):
    pass

# ---------- FLIGHTS ----------
class FlightCreate(BaseModel):
    origin: IATACode
    destination: IATACode
    departure_time: datetime
    arrival_time: datetime
    base_price: float

class FlightOut(FlightCreate):
    id: str
    available_seats: int

# ---------- BOOKINGS ----------
class PassengerInfo(BaseModel):
    full_name: str
    passport: str
    seat: Optional[str] = None

class BookingCreate(BaseModel):
    flight_id: str
    passengers: List[PassengerInfo]

class BookingOut(BaseModel):
    id: str
    flight_id: str
    user_id: str
    status: BookingStatus
    passengers: List[PassengerInfo]

# ---------- PAYMENTS ----------
class PaymentCreate(BaseModel):
    booking_id: str
    amount: float
    payment_method: str

class PaymentOut(BaseModel):
    id: str
    booking_id: str
    status: PaymentStatus

# ---------- AIRCRAFTS ----------
class AircraftCreate(BaseModel):
    tail_number: str = Field(min_length=5, max_length=10)
    model: str
    capacity: int

class AircraftOut(AircraftCreate):
    id: str
