FROM python:3-buster as build

RUN mkdir -p /install
COPY requirements.txt /
RUN pip install --no-warn-script-location --prefix=/install -r /requirements.txt



FROM python:3-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=build /install /usr/local

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD python manage.py runserver 0.0.0.0:8000
