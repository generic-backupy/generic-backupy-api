#!/usr/bin/env sh

# actions which should be do while installation of the module (installing python dependencies, etc.)

# get paths
SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
PACKAGE_FOLDER="${SCRIPTPATH}/.."
REQUIREMENTS="${PACKAGE_FOLDER}/requirements.txt"

# navigate to package folder
cd "$PACKAGE_FOLDER"

# create virtual env
python -m venv venv
source venv/bin/activate

# install requirements
pip install -r "$REQUIREMENTS"

# deactivate venv
deactivate
