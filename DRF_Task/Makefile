
dev-build:
	docker-compose -f docker-compose.dev.yml build

dev-up:
	docker-compose -f docker-compose.dev.yml up
dev-down:
	docker-compose -f docker-compose.dev.yml down

dev-migrations:
	docker-compose -f docker-compose.dev.yml run web python manage.py makemigrations
	docker-compose -f docker-compose.dev.yml run web python manage.py migrate

dev-createsuperuser:
	docker-compose -f docker-compose.dev.yml run web python manage.py createsuperuser

# Production commands
prod-build:
	docker-compose -f docker-compose.prod.yml build

prod-up:
	docker-compose -f docker-compose.prod.yml up
prod-down:
	docker-compose -f docker-compose.prod.yml down

prod-migrations:
	docker-compose -f docker-compose.prod.yml run web python manage.py makemigrations
	docker-compose -f docker-compose.prod.yml run web python manage.py migrate

build:
	docker-compose build
