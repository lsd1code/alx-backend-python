FROM python:3.10

COPY chats /api/
COPY messaging_app /api/
COPY authentication.md /api/
COPY db.sqlite3 /api/
COPY manage.py /api/
COPY post_man-Collections /api/
COPY requirements.txt /api/

WORKDIR /api

RUN pip install --no-cache -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]