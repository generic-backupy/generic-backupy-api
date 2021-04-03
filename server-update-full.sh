#!/bin/sh
git add .
git reset --hard
git pull
./manage.py.prod.sh migrate
./manage.py.prod.sh compilemessages
./manage.py.prod.sh updatepermissions
./run.prod.full.sh
