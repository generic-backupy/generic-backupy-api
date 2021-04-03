./docker-compose.local.sh exec db pg_dumpall -c -U generic-backupy > postgres_dumps/dump_$(date +%Y-%m-%d_%H_%M_%S).sql
