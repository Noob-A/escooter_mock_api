from sqlalchemy.orm import Session

from app import schemas
from app.models import Scooter, Rental
from app.schemas import ScooterCreate, ScooterUpdate, RentalCreate, RentalUpdate

# --- Scooter CRUD ---
def get_scooter(db: Session, scooter_id: int, user_id: int):
    return db.query(Scooter).filter(Scooter.id == scooter_id, Scooter.user_id == user_id).first()

def get_scooters(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Scooter).filter(Scooter.user_id == user_id).offset(skip).limit(limit).all()

def create_scooter(db: Session, scooter: ScooterCreate, user_id: int):
    db_scooter = Scooter(**scooter.dict(), user_id=user_id)
    db.add(db_scooter)
    db.commit()
    db.refresh(db_scooter)
    return db_scooter

def update_scooter(db: Session, scooter_id: int, scooter_data: ScooterUpdate, user_id: int):
    db_scooter = get_scooter(db, scooter_id, user_id)
    if not db_scooter:
        return None
    for key, value in scooter_data.dict(exclude_unset=True).items():
        setattr(db_scooter, key, value)
    db.commit()
    db.refresh(db_scooter)
    return db_scooter

def delete_scooter(db: Session, scooter_id: int, user_id: int):
    db_scooter = get_scooter(db, scooter_id, user_id)
    if not db_scooter:
        return None
    db.delete(db_scooter)
    db.commit()
    return db_scooter

# --- Rental CRUD ---
def get_rental(db: Session, rental_id: int, user_id: int):
    return db.query(Rental).filter(Rental.id == rental_id, Rental.user_id == user_id).first()

def get_rentals(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Rental).filter(Rental.user_id == user_id).offset(skip).limit(limit).all()

def create_rental(db: Session, rental: schemas.RentalCreate, user_id: int):
    db_rental = Rental(**rental.dict(), user_id=user_id)
    db.add(db_rental)
    db.commit()
    db.refresh(db_rental)
    return db_rental

# Note: Do not implement delete_rental for rentals as they are not allowed to be deleted.
