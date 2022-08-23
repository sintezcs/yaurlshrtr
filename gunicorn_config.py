"""Gunicorn basic configuration."""

import os


bind = os.getenv('GUNICORN_BIND', '0.0.0.0:80')

# https://docs.gunicorn.org/en/stable/design.html#how-many-workers
DEFAULT_NUM_WORKERS = 2 * os.cpu_count() + 1
workers = int(os.getenv('GUNICORN_WORKERS', DEFAULT_NUM_WORKERS))
worker_class = os.getenv('GUNICORN_WORKER_CLASS', 'uvicorn.workers.UvicornWorker')
