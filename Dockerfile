# pull official base image
FROM python:3.12-slim-bookworm

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv

# RUN apt-get update && apt-get install -y \
#     gcc \
#     default-libmysqlclient-dev \
#     build-essential \
#     libssl-dev \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# install uv
COPY --from=ghcr.io/astral-sh/uv:0.7.21 /uv /uvx /bin/

# Since there's no point in shipping lock files, we move them
# into a directory that is NOT copied into the runtime image.
# The trailing slash makes COPY create `/_lock/` automagically.
COPY pyproject.toml uv.lock /_lock/

# Synchronize dependencies.
# This layer is cached until uv.lock or pyproject.toml change.
RUN --mount=type=cache,target=/root/.cache \
    cd /_lock && \
    uv sync \
    --frozen \
    --no-install-project

# copy project
COPY . .

# Command de RUN
ENTRYPOINT ["sh", "-c", "uv run manage.py migrate && uv run manage.py runserver 0.0.0.0:8000"]