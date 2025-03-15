# app/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Scooter, Rental
from app.schemas import ScooterCreate, ScooterUpdate, RentalCreate, RentalUpdate

# --- Scooter CRUD ---
async def get_scooter(db: AsyncSession, scooter_id: int, user_id: int):
    result = await db.execute(select(Scooter).where(Scooter.id == scooter_id, Scooter.user_id == user_id))
    return result.scalar_one_or_none()

async def get_scooters(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Scooter).where(Scooter.user_id == user_id).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def create_scooter(db: AsyncSession, scooter: ScooterCreate, user_id: int):
    db_scooter = Scooter(**scooter.dict(), user_id=user_id)
    db.add(db_scooter)
    await db.commit()
    await db.refresh(db_scooter)
    return db_scooter

async def update_scooter(db: AsyncSession, scooter_id: int, scooter_data: ScooterUpdate, user_id: int):
    db_scooter = await get_scooter(db, scooter_id, user_id)
    if not db_scooter:
        return None
    for key, value in scooter_data.dict(exclude_unset=True).items():
        setattr(db_scooter, key, value)
    await db.commit()
    await db.refresh(db_scooter)
    return db_scooter

async def delete_scooter(db: AsyncSession, scooter_id: int, user_id: int):
    db_scooter = await get_scooter(db, scooter_id, user_id)
    if not db_scooter:
        return None
    await db.delete(db_scooter)
    await db.commit()
    return db_scooter

# --- Rental CRUD ---
async def get_rental(db: AsyncSession, rental_id: int, user_id: int):
    result = await db.execute(select(Rental).where(Rental.id == rental_id, Rental.user_id == user_id))
    return result.scalar_one_or_none()

async def get_rentals(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Rental).where(Rental.user_id == user_id).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def create_rental(db: AsyncSession, rental: RentalCreate, user_id: int):
    db_rental = Rental(**rental.dict(), user_id=user_id)
    db.add(db_rental)
    await db.commit()
    await db.refresh(db_rental)
    return db_rental

async def update_rental(db: AsyncSession, rental_id: int, rental_data: RentalUpdate, user_id: int):
    db_rental = await get_rental(db, rental_id, user_id)
    if not db_rental:
        return None
    for key, value in rental_data.dict(exclude_unset=True).items():
        setattr(db_rental, key, value)
    await db.commit()
    await db.refresh(db_rental)
    return db_rental

# Deletion for rentals is not allowed.

async def count_active_rentals(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Rental).where(Rental.user_id == user_id, Rental.is_finished == False)
    )
    active_rentals = result.scalars().all()
    return len(active_rentals)
