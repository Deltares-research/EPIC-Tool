#!/bin/sh

# Author : Carles S. Soriano Perez (carles.sorianoperez@deltares.nl)
python3 -c "import secrets; from pathlib import Path; Path('.django_secrets').write_text(secrets.token_hex(16))"
python3 -c "from pathlib import Path; Path('.django_debug').write_text('True')"
poetry install
poetry run python3 manage.py epic_setup --test
poetry run python3 manage.py collectstatic --noinput
poetry run gunicorn epic_core.wsgi &