# Carga y exporta variables desde .env
include .env
export $(shell sed 's/=.*//' .env)

# Define los servicios de Docker Compose
DB_SERVICE = postgres_db
LOADER_SERVICE = loader
API_SERVICE = api
DOWNLOADER_SERVICE = downloader

all: up

build:
	docker-compose --profile all build

# Crea todos los contenedores de Docker y inica los de API y Postgres
up:
	docker-compose --profile all up -d --no-start
	docker-compose --profile manual up -d

down:
	docker-compose --profile all down

restart: down up

dev: build
	docker-compose --profile all up --no-start
	docker-compose --profile manual up

dev-all: build
	docker-compose --profile all up

open-db:
	docker exec -it $(DB_SERVICE) psql -U $(POSTGRES_USER) $(POSTGRES_DB)

open-loader:
	docker exec -it $(LOADER_SERVICE) bash

open-api:
	docker exec -it $(API_SERVICE) bash

open-downloader:
	docker exec -it $(DOWNLOADER_SERVICE) bash

logs:
	docker-compose --profile all logs -f

ps:
	docker-compose --profile all ps

.PHONY: all build up down restart dev dev-all open-db open-loader open-api open-downloader logs ps