FROM python:3.7

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

#ENV C_FORCE_ROOT=1

COPY app /app
RUN  poetry install --no-root --no-dev

ENV PYTHONPATH=/app

CMD bash celery worker -A app.worker -l info -Q batch-upload -c 1
