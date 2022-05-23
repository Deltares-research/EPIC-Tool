#!/bin/sh

# Author : Carles S. Soriano Perez (carles.sorianoperez@deltares.nl)
python -c "import secrets; from pathlib import Path; Path('.django_secrets').write_text(secrets.token_hex(16))"
python -c "from pathlib import Path; Path('.django_debug').write_text('False')"
poetry run python3 manage.py epic_setup
poetry run python3 manage.py collectstatic --noinput
poetry run gunicorn epic_setup.wsgi &