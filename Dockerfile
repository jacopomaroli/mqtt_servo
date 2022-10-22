# Built following https://sourcery.ai/blog/python-docker/

FROM --platform=$TARGETPLATFORM python:3.9.0-alpine as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apk add build-base

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install RPi.GPIO

FROM python-deps AS runtime

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

WORKDIR /app
COPY ./src .

ENTRYPOINT [ "python3", "mqtt_servo.py"]