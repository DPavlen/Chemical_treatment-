FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=backend.settings
ENV DJANGO_CONFIGURATION=Production

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    libjpeg-dev \
    zlib1g-dev \
    libffi-dev \
    libfreetype6-dev \
    liblcms2-dev \
    fontconfig \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

COPY . .

WORKDIR /app/backend

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
