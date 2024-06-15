build:
	docker compose -f local.yml up --build -d --remove-orphans

up:
	docker compose -f local.yml up -d

down:
	docker compose -f local.yml down

show-logs:
	docker compose -f local.yml logs

show-logs-api:
	docker compose -f local.yml logs api

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --no-input --clear

start:
	python manage.py runserver

superuser:
	python manage.py createsuperuser

down-v:
	docker compose -f local.yml down -v

volume:
	docker volume inspect src_local_postgres_data

authors-db:
	postgres psql --username=leereal --dbname=microfinex-dev

flake8:
	flake8 .

black-check:
	black --check --exclude=migrations .

black-diff:
	black --diff --exclude=migrations .

black:
	black --exclude=migrations .

isort-check:
	isort . --check-only --skip venv --skip migrations

isort-diff:
	isort . --diff --skip venv --skip migrations

isort:
	isort . --skip venv --skip migrations