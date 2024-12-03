FROM python:3

WORKDIR /project

COPY requirements.txt /project/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /project/
EXPOSE 8000
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]
