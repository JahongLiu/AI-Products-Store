from confluent_kafka import Consumer, KafkaError
import time
import json
from app.ai_book_generation.runner import Runner
import threading


class KafkaConsumer:
    def start_kafka_consumer(self, dev=False):
        # Kafka broker address
        bootstrap_servers = "localhost:9092"

        # Create a Kafka consumer instance
        consumer = Consumer(
            {
                "bootstrap.servers": bootstrap_servers,
                "group.id": "my-group",
                "auto.offset.reset": (  # Read from the beginning of the topic
                    "earliest"
                ),
            }
        )

        topic = "book-requests"
        consumer.subscribe([topic])

        while True:
            msg = consumer.poll(1.0)  # Poll for new messages
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(
                        "Reached end of partition for"
                        f" {msg.topic()} [{msg.partition()}]"
                    )
                else:
                    print(f"Error while consuming message: {msg.error()}")
                continue
            print(f"Received message: key={msg.key()}, value={msg.value()}")
            message_params = json.loads(msg.value())
            topic = message_params.get("topic")
            target_audience = message_params.get("target_audience")
            recipient_email = message_params.get("recipient_email")
            preview = message_params.get("preview")

            if not dev:
                try:
                    thread = threading.Thread(
                        target=self.fulfill_request,
                        args=(
                            topic,
                            target_audience,
                            recipient_email,
                            preview,
                        ),
                    )
                    thread.start()

                except Exception as e:
                    print(f"Failed to create ebook! {e}")
        consumer.close()

    def fulfill_request(
        self, topic, target_audience, recipient_email, preview
    ):
        unique_id = str(int(time.time())) + "-" + str(threading.get_ident())
        print(f"CALLED WITH ID: {unique_id}")
        try:
            Runner().create_ebook(
                topic,
                target_audience,
                recipient_email,
                preview=preview,
                id=unique_id,
            )
        except Exception as e:
            print(f"Exception occurred: {e}")


if __name__ == "__main__":
    kp = KafkaConsumer()
    kp.start_kafka_consumer(False)
