#!/bin/sh

# Esperar a que PostgreSQL acepte conexiones
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo "PostgreSQL no está listo, esperando 5 segundos..."
  sleep 5
done

echo "PostgreSQL está listo"

exec uvicorn app.main:app --host "$API_HOST" --port "$API_PORT" --reload
