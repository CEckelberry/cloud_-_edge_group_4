FROM python:3.10

WORKDIR /app

COPY ./auth /app
COPY consumer.py /app
RUN pip install confluent_kafka

CMD ["python3", "consumer.py"]