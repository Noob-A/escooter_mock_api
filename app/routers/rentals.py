from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, database, dependencies

router = APIRouter()

@router.get("/", response_model=List[schemas.Rental])
def read_rentals(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(dependencies.get_current_user_id)
):
    rentals = crud.get_rentals(db, user_id=user_id, skip=skip, limit=limit)
    return rentals

@router.post("/", response_model=schemas.Rental)
def create_rental(
    rental: schemas.RentalCreate,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(dependencies.get_current_user_id)
):
    return crud.create_rental(db, rental, user_id)

@router.get("/{rental_id}", response_model=schemas.Rental)
def read_rental(
    rental_id: int,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(dependencies.get_current_user_id)
):
    db_rental = crud.get_rental(db, rental_id, user_id)
    if db_rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    return db_rental

@router.put("/{rental_id}", response_model=schemas.Rental)
def update_rental(
    rental_id: int,
    rental: schemas.RentalUpdate,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(dependencies.get_current_user_id)
):
    db_rental = crud.update_rental(db, rental_id, rental, user_id)
    if db_rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    return db_rental

@router.delete("/{rental_id}", response_model=schemas.Rental)
def delete_rental(
    rental_id: int,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(dependencies.get_current_user_id)
):
    db_rental = crud.delete_rental(db, rental_id, user_id)
    if db_rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    return db_rental
