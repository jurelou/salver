#!/bin/bash

[ -d "./virtualenv" ] && rm -r ./virtualenv
python3 -m venv virtualenv
source ./virtualenv/bin/activate
pip install pip setuptools --upgrade
if [ ! -z "$1" ] && [ "$1" = "--prod" ]; then
  echo "Installing production environment" && pip install .
else
  echo "Installing Developement environment" && pip install -e .
fi
