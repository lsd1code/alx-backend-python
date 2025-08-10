FROM python:3.10

ENV PYTHONNUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install --no-cache -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]