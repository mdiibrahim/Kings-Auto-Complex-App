#!/usr/bin/env bash
set -o errexit  # Error handling (stops if a command fails)

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate
