#!/bin/bash
cd "$(dirname "$0")"
export PATH="$(pwd)/venv/bin:$PATH"
python manage.py runserver
