DB_SERVICE = postgres_db
POSTGRES_USER = admin
POSTGRES_DB = mydb
POSTGRES_PORT = 5432

LOADER_SERVICE = loader
API_SERVICE = api

.PHONY: build up down restart logs ps

all: up

build:
	docker-compose --profile all build

# Create and start all services, but do not start the ones in the "manual" profile
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
	docker-compose exec -it $(DB_SERVICE) psql -U $(POSTGRES_USER) $(POSTGRES_DB)

open-loader:
	docker-compose exec -it $(LOADER_SERVICE) bash

open-api:
	docker-compose exec -it $(API_SERVICE) bash

logs:
	docker-compose --profile all logs -f

ps:
	docker-compose --profile all ps
