# Use an official Python runtime as the base image.
FROM python:3.11-slim

# Set environment variables to disable writing .pyc files and enable unbuffered logging.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies.
RUN apt-get update && apt-get install -y curl build-essential

# Install Poetry.
ENV POETRY_VERSION=2.0.1
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set work directory.
WORKDIR /app

# Copy only pyproject.toml and poetry.lock first for caching.
COPY pyproject.toml poetry.lock ./

# Configure Poetry to not use virtual environments and install dependencies.
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application code.
COPY . .

# Expose the port the app runs on.
EXPOSE 15022

# Run the FastAPI application on port 15022.
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15022", "--root-path", "/api/mock/escooter"]
