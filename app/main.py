from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import scooters, rentals, users

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="eScooter Service API")

app.include_router(scooters.router, prefix="/scooters", tags=["Scooters"])
app.include_router(rentals.router, prefix="/rentals", tags=["Rentals"])
app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the eScooter Service API"}
