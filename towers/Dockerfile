FROM python:buster
ENV PYTHONUNBUFFERED=1
RUN pip3 install pyserial
RUN mkdir /code
COPY . /code
WORKDIR /code
CMD python3 towers.py
