"""Gunicorn configuration."""

import os


bind = os.getenv('GUNICORN_BIND', '0.0.0.0:80')
backlog = int(os.getenv('GUNICORN_BACKLOG', 2048))


workers = int(os.getenv('GUNICORN_WORKERS', 1))
worker_class = os.getenv('GUNICORN_WORKER_CLASS', 'uvicorn.workers.UvicornWorker')
worker_connections = int(os.getenv('GUNICORN_WORKER_CONNECTIONS', 1000))
timeout = int(os.getenv('GUNICORN_TIMEOUT', 30))
keepalive = int(os.getenv('GUNICORN_KEEPALIVE', 2))

# spew = False
#
#
# daemon = False
# pidfile = None
# umask = 0
# user = None
# group = None
# tmp_upload_dir = None
#
#
# errorlog = '-'
# loglevel = 'info'
# accesslog = '-'
# access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
#
# proc_name = None
