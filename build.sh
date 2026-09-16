#!/usr/bin/env sh
set -e

python -m pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py seed_data
python manage.py collectstatic --noinput