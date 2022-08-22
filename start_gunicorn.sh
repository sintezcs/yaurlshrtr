#!/bin/sh

exec /app/.venv/bin/gunicorn -c /app/gunicorn_config.py urlshrtr.app:app
