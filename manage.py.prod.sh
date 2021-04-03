#!/bin/bash
/bin/bash docker-compose.prod.api.sh run --rm api python3 manage.py $@
