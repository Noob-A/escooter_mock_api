import asyncio
from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import scooters, rentals, users


async def init_db():
    async with engine.begin() as conn:
        # run_sync executes the synchronous create_all() using the connection
        await conn.run_sync(Base.metadata.create_all)


# Create the FastAPI app
app = FastAPI(title="eScooter Service API")

# Include routers
app.include_router(scooters.router, prefix="/scooters", tags=["Scooters"])
app.include_router(rentals.router, prefix="/rentals", tags=["Rentals"])
app.include_router(users.router, prefix="/users", tags=["Users"])


@app.on_event("startup")
async def on_startup():
    # Create database tables asynchronously on startup.
    await init_db()


@app.get("/")
async def read_root():
    return {"message": "Welcome to the eScooter Service API"}


if __name__ == "__main__":
    # For running the app directly (e.g. via 'python app/main.py')
    asyncio.run(init_db())
