./manage.py.prod.sh collectstatic --noinput
./docker-compose.prod.api.sh up --build -d
docker exec generic-backupy-api sh run_qcluster.sh
