FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTEECODE=1

ENV PYTHONNUNBUFFERED=1

WORKDIR /app

RUN apt update && apt upgrade

RUN apt-get install -y curl

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY ./requirements.txt .

RUN uv pip install -r requirements.txt --system

COPY . .

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]