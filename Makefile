DC = docker compose

build:
	$(DC) build

rebuild:
	$(DC) down
	$(DC) build --no-cache
	$(DC) up -d --remove-orphans

up:
	$(DC) up -d

down:
	$(DC) down

restart:
	$(DC) restart

restart-api:
	$(DC) restart equipment-rent

logs:
	$(DC) logs -f

logs-api:
	$(DC) logs -f equipment-rent

logs-db:
	$(DC) logs -f rent-postgres

ps:
	$(DC) ps

shell:
	$(DC) exec equipment-rent bash

migrate-init:
	$(DC) exec equipment-rent aerich init -t migrations.config.TORTOISE_ORM

migrate-init-db:
	$(DC) exec equipment-rent aerich init-db

migrate:
	$(DC) exec equipment-rent aerich migrate

migrate-upgrade:
	$(DC) exec equipment-rent aerich upgrade