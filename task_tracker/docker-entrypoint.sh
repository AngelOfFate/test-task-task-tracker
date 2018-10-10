#!/bin/bash

set -e
set -x

# Define help message
show_help() {
    echo """
Usage: docker run <imagename> COMMAND

Commands

dev       : Run Django development server
python    : Run Python command
bash      : Run bash shell
test      : Run tests
help      : Show this message
manage    : Run manage command for project
init_base : Load init.json from fixtures dir for project
"""
}

setup_db() {
    python manage.py makemigrations task_tracker
    python manage.py migrate
}

run_dev_server() {
    setup_db
    python manage.py runserver 0.0.0.0:8000
}

# Run
case "$1" in
    dev)
        run_dev_server
    ;;
    init_base)
        python manage.py loaddata fixtures/init.json
    ;;
    python)
        python "${@:2}"
    ;;
    bash)
        /bin/bash "${@:2}"
    ;;
    manage)
        python manage.py "${@:2}"
    ;;
    *)
        show_help
    ;;
esac
