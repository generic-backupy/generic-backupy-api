#!/usr/bin/env sh

for d in /packages/*/docker-build-hook.sh ; do
    echo "execute package docker-build script ${d}"
    /bin/sh "$d"
done
