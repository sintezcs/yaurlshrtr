FROM python:3.9-slim

WORKDIR /app

# install poetry
RUN python -m pip install poetry

# add the requirements to the container
COPY poetry.lock pyproject.toml /app/

# install the requirements
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# we are also installing the dev requirements here for simplicity
# in a real-life project a multi-stage docker build would be a better solution
RUN poetry install --no-root --no-interaction

# install gunicorn
RUN poetry add gunicorn

# add the application to the container
COPY src/ /app/

# add gunicorn startup script and config file to the container
COPY gunicorn_config.py start_gunicorn.sh run_tests.sh /app/

# expose port 80
EXPOSE 80

# run gunicorn
CMD ["/app/start_gunicorn.sh"]
