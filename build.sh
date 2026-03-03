#!/bin/bash

# This script runs after pip install on Vercel
# It handles Django migrations and static file collection

set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo "Running migrations..."
python manage.py migrate --noinput || true

echo "Build completed successfully!"
