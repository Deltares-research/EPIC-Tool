#!/bin/sh

# Author : Carles S. Soriano Perez (carles.sorianoperez@deltares.nl)
git pull
poetry install
poetry run python3 manage.py makemigrations
poetry run python3 manage.py migrate
poetry run python3 manage.py collectstatic --noinput
poetry run gunicorn epic_core.wsgi &