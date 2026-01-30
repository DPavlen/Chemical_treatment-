.PHONY: build up down restart logs shell migrate makemigrations createsuperuser collectstatic clean

# Build containers
build:
	docker compose build

# Start containers
up:
	docker compose up -d

# Stop containers
down:
	docker compose down

# Restart containers
restart: down up

# View logs
logs:
	docker compose logs -f

# Backend logs only
logs-backend:
	docker compose logs -f backend

# Shell into backend container
shell:
	docker compose exec backend bash

# Django shell
django-shell:
	docker compose exec backend python manage.py shell

# Run migrations
migrate:
	docker compose exec backend python manage.py migrate

# Create migrations
makemigrations:
	docker compose exec backend python manage.py makemigrations

# Create superuser
createsuperuser:
	docker compose exec backend python manage.py createsuperuser

# Collect static files
collectstatic:
	docker compose exec backend python manage.py collectstatic --noinput

# Remove containers and volumes
clean:
	docker compose down -v --remove-orphans

# Rebuild and start
rebuild: down build up

# Show container status
ps:
	docker compose ps
