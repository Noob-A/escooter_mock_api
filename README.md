# eScooter Mock API

A fully asynchronous FastAPI service that simulates an e‑scooter rental system. This project demonstrates a real-world-like API with user-specific scooter and rental management, including endpoints for generating random data with configurable failure scenarios.

## Features

- **Async API Endpoints:** Built using FastAPI with asynchronous endpoints.
- **User-Specific Data:** Each user (identified via a simple header) can only access and manage their own scooters and rentals.
- **Rental Management:** Create, view, and end rentals. Active (unfinished) rentals are limited to three per user.
- **Random Data Generation:** A dedicated endpoint generates random scooter and rental data using the Faker library, with customizable payment failure scenarios.
- **PostgreSQL Integration:** Uses PostgreSQL as the backend database via SQLAlchemy's async engine.
- **Docker & Docker Compose:** Preconfigured Dockerfile and docker-compose setup for easy deployment.

## Project Structure

```
escooter-mock-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── dependencies.py
│   └── routers/
│       ├── __init__.py
│       ├── scooters.py
│       ├── rentals.py
│       └── users.py
├── pyproject.toml
├── poetry.lock
├── Dockerfile
└── docker-compose.yml
```

## Requirements

- Python 3.11 or higher
- [Poetry](https://python-poetry.org/) for dependency management
- Docker & Docker Compose (optional, for containerized deployment)

## Installation

### Using Poetry

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Noob-A/escooter-mock-api.git
   cd escooter-mock-api
   ```

2. **Install Dependencies:**

   ```bash
   poetry install
   ```

3. **Run the Application:**

   ```bash
   poetry run uvicorn app.main:app --host 0.0.0.0 --port 15022
   ```

### Using Docker Compose

1. **Build and Run the Containers:**

   ```bash
   docker-compose up --build
   ```

   This will build the FastAPI application container and a PostgreSQL container. The API will be available on port `15022`.

2. **Environment Configuration:**

   The application reads its database connection from the `DATABASE_URL` environment variable. In the provided `docker-compose.yml`, it is configured as:
   
   ```
   DATABASE_URL: "postgresql+asyncpg://postgres:postgres@db:5432/escooter"
   ```

## Configuration

The project configuration is handled in `app/config.py`. Here you can set:

- **CITY:** The city used to generate street addresses (e.g., `"Moscow"`).
- **FAILURE_CHANCE_PERCENT:** Percentage chance (0-100) that a rental payment will fail.
- **FAILURE_REASONS:** A list of possible failure reasons.
- **FAKER_LOCALE:** Used for street generation
Example:

```python
# Specify the city used for generating street addresses.
CITY = "Moscow"
FAKER_LOCALE='ru'

# Percentage chance (0-100) that a rental payment will fail.
FAILURE_CHANCE_PERCENT = 30

# List of possible failure reasons.
FAILURE_REASONS = [
    "недостаточный баланс на вашем счете",
    "техническая ошибка платежной системы",
    "лимит по расходам превышен",
    "банковская карта недействительна",
    "ошибка при верификации платежных данных"
]
```

## API Endpoints

### User Endpoints

- **POST /users/generate**  
  Generates random scooter and rental data for the current user. Requires the `X-User-ID` header.

### Scooter Endpoints

- **GET /scooters/** – List scooters for the current user.
- **POST /scooters/** – Create a new scooter.
- **GET /scooters/{scooter_id}** – Retrieve a specific scooter.
- **PUT /scooters/{scooter_id}** – Update a scooter.
- **DELETE /scooters/{scooter_id}** – Delete a scooter.

### Rental Endpoints

- **GET /rentals/** – List rentals for the current user.
- **POST /rentals/** – Create a new rental (active rentals limited to three per user).
- **GET /rentals/{rental_id}** – Retrieve a specific rental.
- **POST /rentals/{rental_id}/end** – End a rental. Once ended, rentals cannot be deleted.

_Note: Every request must include an `X-User-ID` header to identify the user._

## Database Initialization

The database tables are created on startup using an asynchronous connection. Check `app/main.py` for the startup event that runs the schema creation.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/yourusername/escooter-mock-api/issues) if you want to contribute.

## License

Distributed under the MIT License. See `LICENSE` for more information.

