from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, database, dependencies

router = APIRouter()

@router.get("/", response_model=List[schemas.Scooter])
def read_scooters(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(dependencies.get_current_user_id)
):
    scooters = crud.get_scooters(db, user_id=user_id, skip=skip, limit=limit)
    return scooters

@router.post("/", response_model=schemas.Scooter)
def create_scooter(
    scooter: schemas.ScooterCreate,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(dependencies.get_current_user_id)
):
    return crud.create_scooter(db, scooter, user_id)

@router.get("/{scooter_id}", response_model=schemas.Scooter)
def read_scooter(
    scooter_id: int,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(dependencies.get_current_user_id)
):
    db_scooter = crud.get_scooter(db, scooter_id, user_id)
    if db_scooter is None:
        raise HTTPException(status_code=404, detail="Scooter not found")
    return db_scooter

@router.put("/{scooter_id}", response_model=schemas.Scooter)
def update_scooter(
    scooter_id: int,
    scooter: schemas.ScooterUpdate,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(dependencies.get_current_user_id)
):
    db_scooter = crud.update_scooter(db, scooter_id, scooter, user_id)
    if db_scooter is None:
        raise HTTPException(status_code=404, detail="Scooter not found")
    return db_scooter

@router.delete("/{scooter_id}", response_model=schemas.Scooter)
def delete_scooter(
    scooter_id: int,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(dependencies.get_current_user_id)
):
    db_scooter = crud.delete_scooter(db, scooter_id, user_id)
    if db_scooter is None:
        raise HTTPException(status_code=404, detail="Scooter not found")
    return db_scooter
