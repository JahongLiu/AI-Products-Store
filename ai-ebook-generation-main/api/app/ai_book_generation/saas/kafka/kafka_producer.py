import json
from confluent_kafka import Producer
from flask import jsonify


class KafkaProducer:
    def kafka_add_to_topic(
        self, topic, target_audience, recipient_email, preview=False
    ):
        # Kafka broker address
        bootstrap_servers = "localhost:9092"
        producer = Producer({"bootstrap.servers": bootstrap_servers})

        message_params = {
            "topic": topic,
            "target_audience": target_audience,
            "recipient_email": recipient_email,
            "preview": preview,
            # Add more parameters as needed
        }
        message_value = json.dumps(message_params)
        producer.produce("book-requests", key=None, value=message_value)
        producer.flush()

        return jsonify(
            {
                "message": (
                    f"Successfully added to request queue for topic: {topic},"
                    f" target_audience: {target_audience}"
                )
            }
        )


if __name__ == "__main__":
    kp = KafkaProducer()
    kp.kafka_add_to_topic("test", "test")
