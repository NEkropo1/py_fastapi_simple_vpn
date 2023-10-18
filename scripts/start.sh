#!/bin/bash

wait_for_db() {
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
        echo "Waiting for database to start..."
        sleep 1
    done
    echo "Database is ready!"
}

wait_for_db
# Run database migrations
alembic revision --autogenerate -m "First migration"
alembic upgrade head

# Start the FastAPI application
uvicorn main:app --host 0.0.0.0 --port 8000
