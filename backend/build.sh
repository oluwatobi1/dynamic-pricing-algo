#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r backend/requirements.txt


# Convert static asset files
python backend/manage.py collectstatic --no-input

# Apply any outstanding database migrations
python backend/manage.py migrate