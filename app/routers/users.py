from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
from faker import Faker

from app import crud, schemas, database, dependencies
from app.config import CITY, FAILURE_CHANCE_PERCENT, FAILURE_REASONS

router = APIRouter()
fake = Faker(locale='ru')


@router.post("/generate", response_model=dict)
def generate_random_data(
        db: Session = Depends(database.get_db),
        user_id: int = Depends(dependencies.get_current_user_id)
):
    # Check if user already has 3 active rentals.
    if crud.count_active_rentals(db, user_id) >= 3:
        raise HTTPException(status_code=400, detail="Maximum number of active rentals reached")

    # Generate random scooter data.
    scooter_models = ["P12", "X20", "E5", "S3"]
    scooter_location = f"{fake.street_address()}, {CITY}"
    random_scooter = schemas.ScooterCreate(
        model=random.choice(scooter_models),
        location=scooter_location
    )
    created_scooter = crud.create_scooter(db, random_scooter, user_id)

    # Generate random rental data.
    now = datetime.utcnow()
    start_time = now - timedelta(hours=random.randint(1, 5))
    end_time = start_time + timedelta(hours=1)

    if random.randint(1, 100) <= FAILURE_CHANCE_PERCENT:
        payment_status = "failed"
        failure_reason = random.choice(FAILURE_REASONS)
    else:
        payment_status = "paid"
        failure_reason = None

    start_location = f"{fake.street_address()}, {CITY}"
    end_location = f"{fake.street_address()}, {CITY}"
    random_rental = schemas.RentalCreate(
        scooter_id=created_scooter.id,
        start_time=start_time,
        end_time=end_time,
        start_location=start_location,
        end_location=end_location,
        payment_status=payment_status,
        failure_reason=failure_reason
    )
    created_rental = crud.create_rental(db, random_rental, user_id)

    return {
        "scooter": schemas.Scooter.model_validate(created_scooter),
        "rental": schemas.Rental.model_validate(created_rental)
    }
