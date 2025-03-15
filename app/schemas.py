from datetime import datetime
from pydantic import BaseModel

# --- Scooter Schemas ---
class ScooterBase(BaseModel):
    model: str
    location: str

class ScooterCreate(ScooterBase):
    pass

class ScooterUpdate(BaseModel):
    battery_level: float = None
    is_available: bool = None
    location: str = None

class Scooter(ScooterBase):
    id: int
    user_id: int
    battery_level: float
    is_available: bool
    last_maintenance: datetime

    class Config:
        from_attributes = True

# --- Rental Schemas ---
class RentalBase(BaseModel):
    scooter_id: int
    start_time: datetime
    end_time: datetime
    start_location: str
    end_location: str

class RentalCreate(RentalBase):
    payment_status: str = "pending"
    failure_reason: str | None = None
    # Note: is_finished is set by the DB and defaults to False.

class RentalUpdate(BaseModel):
    payment_status: str = None
    failure_reason: str | None = None
    # Not allowing direct update of is_finished through this schema.

class Rental(RentalBase):
    id: int
    user_id: int
    payment_status: str
    failure_reason: str | None = None
    is_finished: bool
    scooter: Scooter

    class Config:
        from_attributes = True
