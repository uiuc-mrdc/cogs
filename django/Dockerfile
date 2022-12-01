FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
ENTRYPOINT ["./docker-entrypoint.sh"]
# By default, start the Gunicorn server with eight Uvicorn workers
CMD ["gunicorn", "composeexample.asgi:application", "--bind=0.0.0.0:8000", "--workers=8", "--worker-class=uvicorn.workers.UvicornWorker"]
