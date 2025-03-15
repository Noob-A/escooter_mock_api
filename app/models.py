from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Scooter(Base):
    __tablename__ = "scooters"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, index=True)
    battery_level = Column(Float, default=100.0)
    is_available = Column(Boolean, default=True)
    location = Column(String, default="unknown")
    last_maintenance = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, nullable=False, index=True)

    rentals = relationship("Rental", back_populates="scooter")


class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)
    scooter_id = Column(Integer, ForeignKey("scooters.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    start_location = Column(String, nullable=False)
    end_location = Column(String, nullable=False)
    payment_status = Column(String, default="pending")
    failure_reason = Column(String, nullable=True)
    user_id = Column(Integer, nullable=False, index=True)

    scooter = relationship("Scooter", back_populates="rentals")
