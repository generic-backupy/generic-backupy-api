docker compose -f docker-compose.yml -f docker-compose.prod.yml run --rm api python3 manage.py migrate
docker compose -f docker-compose.yml -f docker-compose.prod.yml run --rm api python3 manage.py createsuperuser
