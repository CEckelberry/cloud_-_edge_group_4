FROM python:3.10

WORKDIR /app

COPY ./auth /app
COPY consumer.py /app
RUN pip install confluent_kafka click fastavro

VOLUME [ "/app" ]

ENTRYPOINT ["python3", "-u", "consumer.py", "group4"]