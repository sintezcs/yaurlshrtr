#!/bin/sh

set -e

/app/.venv/bin/flake8 /app --exclude .venv
/app/.venv/bin/python -m pytest /app/tests/

