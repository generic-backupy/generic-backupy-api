./docker-compose.prod.api.sh run --rm api python3 manage.py migrate
./docker-compose.prod.api.sh run --rm api python3 manage.py createsuperuser
