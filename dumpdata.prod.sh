#!/bin/bash
./manage.py.prod.sh dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > dump.json
