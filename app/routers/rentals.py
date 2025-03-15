from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app import crud, schemas, database, dependencies

router = APIRouter()


@router.get("/", response_model=list[schemas.Rental])
def read_rentals(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(database.get_db),
        user_id: int = Depends(dependencies.get_current_user_id)
):
    rentals = crud.get_rentals(db, user_id=user_id, skip=skip, limit=limit)
    return [schemas.Rental.model_validate(r) for r in rentals]


@router.post("/", response_model=schemas.Rental)
def create_rental(
        rental: schemas.RentalCreate,
        db: Session = Depends(database.get_db),
        user_id: int = Depends(dependencies.get_current_user_id)
):
    if crud.count_active_rentals(db, user_id) >= 3:
        raise HTTPException(status_code=400, detail="Maximum number of active rentals reached")

    created_rental = crud.create_rental(db, rental, user_id)
    return schemas.Rental.model_validate(created_rental)


@router.get("/{rental_id}", response_model=schemas.Rental)
def read_rental(
        rental_id: int,
        db: Session = Depends(database.get_db),
        user_id: int = Depends(dependencies.get_current_user_id)
):
    rental = crud.get_rental(db, rental_id, user_id)
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    return schemas.Rental.model_validate(rental)


@router.post("/{rental_id}/end", response_model=schemas.Rental)
def end_rental(
        rental_id: int,
        db: Session = Depends(database.get_db),
        user_id: int = Depends(dependencies.get_current_user_id)
):
    rental = crud.get_rental(db, rental_id, user_id)
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    if rental.is_finished:
        raise HTTPException(status_code=400, detail="Rental is already finished")

    rental.is_finished = True
    rental.end_time = datetime.utcnow()  # Update end_time to current time.
    db.commit()
    db.refresh(rental)
    return schemas.Rental.model_validate(rental)
