FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY ./pyproject.toml ./

RUN pip install poetry && poetry self add poetry-plugin-shell

COPY . .

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

EXPOSE 8000


CMD ["poetry", "run", "python", "app/manage.py", "runserver", "0.0.0.0:8000"]

# CMD ["poetry", "run", "gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]