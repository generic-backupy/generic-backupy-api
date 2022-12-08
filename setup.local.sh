./docker-compose.local.sh run --rm api python3 manage.py migrate
./docker-compose.local.sh run --rm api python3 manage.py createsuperuser
