./manage.py.prod.sh collectstatic --noinput
./docker-compose.prod.api.sh up --build -d
