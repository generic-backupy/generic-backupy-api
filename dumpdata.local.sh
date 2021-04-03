#!/bin/bash
./manage.py.local.sh dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > dump.json
