#!/bin/sh

# Esperar a que downloader termine
while [ ! -f $DATA_DIR/downloader.done ]; do
  echo "$DATA_DIR/downloader.done no encontrado, esperando a que el downloader termine..."
  echo "Esperando a que downloader termine..."
  sleep 5
done

# Eliminar el archivo de señalización del downloader
rm $DATA_DIR/downloader.done

echo "Downloader finalizado, comprobando conexión a PostgreSQL..."

# Esperar a que PostgreSQL acepte conexiones
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo "PostgreSQL no está listo, esperando 5 segundos..."
  sleep 5
done

echo "PostgreSQL está listo, comenzando la carga..."

exec python main.py
