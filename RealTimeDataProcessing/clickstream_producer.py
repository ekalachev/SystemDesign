import logging
from kafka import KafkaProducer
from faker import Faker
import json
import random
import string
import time

# Enable logging
logging.basicConfig(level=logging.DEBUG)

fake = Faker()


def generate_random_string(length=10):
    characters = string.ascii_lowercase + string.digits  # 'a-z' and '0-9'
    return ''.join(random.choice(characters) for _ in range(length))


# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9093',  # Change to port 9093
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    retries=5,
    request_timeout_ms=20000,
    retry_backoff_ms=5000
)


def generate_click():
    return {
        'user_id': fake.uuid4(),
        'page': fake.url(),
        'timestamp': fake.iso8601(),
        'action': fake.random_element(elements=('click', 'scroll', 'hover')),
        'session_id': generate_random_string(100)
    }


if __name__ == "__main__":
    topic = 'website_clicks'
    while True:
        click_event = generate_click()
        future = producer.send(topic, click_event)
        try:
            result = future.get(timeout=10)
            print(f"Sent: {click_event}, Result: {result}")
        except Exception as e:
            print(f"Failed to send message: {e}")
        time.sleep(1)
