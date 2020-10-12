FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD python manage.py runserver 0.0.0.0:8000
# CMD daphne -b 0.0.0.0 -p 8000 PHOAN.asgi:application
