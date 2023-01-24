#!/usr/bin/env sh

for f in /packages/*/docker-build-hook.sh ; do
    if [ -f "$f" ];
    then
        echo "execute package docker-build script ${f}"
        /bin/sh "$f"
    fi
done
