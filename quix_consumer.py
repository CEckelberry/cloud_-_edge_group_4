import quix
import json
from dataclasses import dataclass

@dataclass
class ExperimentConfig:
    experiment: str
    researcher: str
    sensors: list[str]
    temperature_range: dict[str, float]

def decode_kafka_message(message):
    """Decodes a Kafka message in Avro format.

    Args:
        message: A Kafka message.

    Returns:
        An ExperimentConfig object.
    """

    schema = {
        "type": "record",
        "name": "ExperimentConfig",
        "fields": [
            {
                "type": "string",
                "name": "experiment"
            },
            {
                "type": "string",
                "name": "researcher"
            },
            {
                "name": "sensors",
                "type": {
                    "type": "array",
                    "items": "string"
                }
            },
            {
                "name": "temperature_range",
                "type": {
                    "type": "record",
                    "name": "temperature_range",
                    "fields": [
                        {"name": "upper_threshold", "type": "float"},
                        {"name": "lower_threshold", "type": "float"}
                    ]
                }
            }
        ]
    }

    decoder = quix.BinaryDecoder(message)
    reader = quix.AvroReader(schema, decoder)
    experiment_config = ExperimentConfig(**reader.read())

    return experiment_config

# Consume Kafka messages from the <team_id> topic
consumer = quix.KafkaConsumer(
    bootstrap_servers="localhost:9092",
    group_id="temperature-observability-microservice",
    topic="<team_id>"
)

# Decode each message and process it
while True:
    message = consumer.poll(timeout=1)
    if message is None:
        continue

    experiment_config = decode_kafka_message(message.value)

    # Process the experiment configuration
    print(f"Experiment configuration: {experiment_config}")
