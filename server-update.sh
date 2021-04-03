#!/bin/sh
git add .
git reset --hard
git pull
./manage.py.prod.sh compilemessages
./run.prod.sh
