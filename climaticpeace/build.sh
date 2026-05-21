#!/usr/bin/env bash
# Exit immediately if any command fails
set -o errexit

pip install -r requirements.txt

# Create static dir if it doesn't exist (prevents collectstatic crash)
mkdir -p static

python manage.py collectstatic --noinput

python manage.py migrate
