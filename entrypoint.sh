#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
# http://stackoverflow.com/questions/19622198/what-does-set-e-mean-in-a-bash-script
set -e


# Define help message
show_help() {
    echo """
    Entrypoint Commands Service:

    poetry_add           : Add and install a dependency with poetry
    poetry_lock          : Create a poetry.lock file with poetry
    shell                : Start a bash shell
    create_db            : Initialize the database
    migrate              : Run django migrations
    runserver            : Collect static files, run migrations and run the Django development server
    dummy_data           : Run dummy_data script for test data
    manage_py [args...]  : Execute a command with manage.py
    python [args...]     : Run internal python
    test                 : Run Django tests
    coverage             : Generate a testing code coverage report
    lint                 : Run the linter on the code and show results
    gunicorn             : Run Django with the gunicorn server
    help                 : Show this message
    celery               : Run celery worker
    flower               : Run flower monitor
"""
}

project_dir=/code
mkdir -p ${project_dir}/test_results

wait_for_db () {
  while ! nc -z "${DB_HOST}" "${DB_PORT}";
  do
    echo "Waiting for DB to be ready"
    sleep 2;
  done
}


wait_for_celery () {
  until celery -A backend inspect ping; do
      >&2 echo "Celery workers not available"
      sleep 5
  done
}

case "$1" in
  poetry_add)
    poetry config virtualenvs.create false
    poetry add "$2"
    poetry install
  ;;
  poetry_lock)
    poetry config virtualenvs.create false
    poetry lock
  ;;
  poetry_install)
    poetry config virtualenvs.create false
    poetry install
  ;;
  create_db)
    wait_for_db
    python manage.py create_db
  ;;
  migrator_task)
    wait_for_db
    python manage.py collectstatic --noinput
    python manage.py migrate
  ;;
  makemigrations)
    wait_for_db
    python manage.py makemigrations
  ;;
  makemigrations_merge)
    wait_for_db
    python manage.py makemigrations --merge
  ;;
  migrate)
    wait_for_db
    python manage.py migrate
  ;;
  migration_check)
    wait_for_db
    ddtrace-run python manage.py migration_check
  ;;
  dummy_data)
    wait_for_db
    python manage.py jummy_data "$2"
  ;;
  runserver)
    wait_for_db
    python manage.py collectstatic --noinput
    python manage.py migrate
    watchmedo auto-restart --directory=./ --patterns="*.py;.env" --recursive -- python manage.py runserver 0.0.0.0:8000 --noreload
  ;;
  gunicorn)
    wait_for_db
    gunicorn backend.wsgi:application \
      --workers 4 \
      --bind 0.0.0.0:8080 \
      --log-level debug \
      --timeout $TIMEOUT
  ;;
  celery)
    shift 1
    if [ "$IS_LOCAL" = "True" ];
    then
      watchmedo auto-restart --directory=./ --patterns="*.py;.env" --recursive -- celery "$@"
    else
       ddtrace-run celery "$@"
    fi
    ;;
  flower)
    wait_for_celery
    shift 1
    celery flower -A backend "$@"
    ;;
  manage_py)
      shift 1
      python manage.py "$@"
  ;;
  python)
      shift 1
      python "$@"
  ;;
  shell)
      bash
  ;;
  test)
      echo "Starting entrypoint.sh:test"
      wait_for_db
      echo "Running Applications Tests: $2"
      IS_TESTING=true pytest "$2" --full-trace
  ;;
  test-keep-db)
      echo "Starting entrypoint.sh:test"
      wait_for_db
      echo "Running Applications Tests: $2"
      IS_TESTING=true pytest "$2" --full-trace --reuse-db
  ;;
  coverage)
      wait_for_db
      coverage erase
      coverage run --source='.' manage.py test
      coverage report
      coverage html -d ${project_dir}/test_results/htmlcov
  ;;
  lint)
      pylint rest_api backend | tee ${project_dir}/test_results/pylint.txt
      exit "${PIPESTATUS[0]}"
  ;;
  *)
      show_help
  ;;
esac
