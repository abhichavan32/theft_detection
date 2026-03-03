#!/bin/bash

# This script runs after pip install on Vercel
# It handles Django migrations and static file collection

python manage.py collectstatic --noinput
python manage.py migrate --noinput
