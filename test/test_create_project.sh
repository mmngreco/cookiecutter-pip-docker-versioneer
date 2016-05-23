#!/bin/bash

# based on https://github.com/audreyr/cookiecutter-pypackage/

set -e

TOXENV=$1

DEPLOY=1
if [ -z "$2" ]
  then
    DEPLOY=0
fi

require() {
    type $1 >/dev/null 2>/dev/null
}

cleanup() {
    rm -rf name-of-the-project
}
trap cleanup EXIT


require cookiecutter

echo "Running test script..."
cookiecutter . --no-input
(
    cd ./name-of-the-project
    export HOME=`pwd`
    git config --global user.email "you@example.com"
    git config --global user.name "Your Name"
    git init .
    git add -A .
    git commit -m "initial."
    pip install versioneer
    pip install -r requirements.txt
    versioneer install
    PYTHONPATH=. python name_of_the_project/run_name_of_the_project.py --help
    PYTHONPATH=. python name_of_the_project/run_name_of_the_project.py --version
    PYTHONPATH=. python name_of_the_project/run_name_of_the_project.py
    PYTHONPATH=. python name_of_the_project/run_name_of_the_project.py --verbose
    tox -e $TOXENV -- -n 8
    if [ "DEPLOY" ]
    then
        echo "TODO REPO DEPLOY"
    fi
)

echo Done
