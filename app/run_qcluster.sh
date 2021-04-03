#!/bin/bash

# maybe check if db is ready, and do a while loop with waits until that moment
echo "kill $(<qcluster.pid)"

# kill process with pid id of file
kill "$(<qcluster.pid)"

# execute and save pid id in file
python3 manage.py qcluster > /dev/null 2>&1 &
echo $! > qcluster.pid
echo "new one $(<qcluster.pid)"
