#!/bin/bash

if [[ "$OSTYPE" == "darwin"* ]]; then
  sed -i '' -e 's#/code#app#g' app/coverage.xml
else
  sed -i -e 's#/code#app#g' app/coverage.xml
fi
