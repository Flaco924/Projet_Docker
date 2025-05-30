#!/bin/bash
# Wait until PostgreSQL is ready
until pg_isready -h db -p 5432 -U user; do
  echo "⏳ Waiting for PostgreSQL..."
  sleep 2
done

# Then launch your app
echo "✅ PostgreSQL is up - starting the API"
exec uvicorn main:app --host 0.0.0.0 --port 8000
