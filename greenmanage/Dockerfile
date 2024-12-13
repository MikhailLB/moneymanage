FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "greenmanage.wsgi:application", "--bind", "0.0.0.0:8000"]
