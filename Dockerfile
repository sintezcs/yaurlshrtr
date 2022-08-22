FROM python:3.9-slim

WORKDIR /app

# install poetry
RUN python -m pip install poetry

# add the requirements to the container
COPY poetry.lock pyproject.toml /app/

# install the requirements
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
RUN poetry install --no-dev --no-root --no-interaction

# install gunicorn
RUN poetry add gunicorn

# add the application to the container
COPY src/urlshrtr /app/urlshrtr

# add gunicorn startup script and config file to the container
COPY gunicorn_config.py start_gunicorn.sh /app/

# expose port 80
EXPOSE 80

# run uvicorn
CMD ["/app/start_gunicorn.sh"]
