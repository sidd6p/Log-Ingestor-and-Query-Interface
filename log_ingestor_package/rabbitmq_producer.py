# rabbitmq_producer.py
import pika
import json

class RabbitMQProducer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        # self.connection = pika.BlockingConnection(pika.ConnectionParameters(config.settings.RABBITMQ_URL))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="logs")

    def publish_log(self, log):
        self.channel.basic_publish(
            exchange="", routing_key="logs", body=json.dumps(log.dict())
        )

rabbitmq_producer = RabbitMQProducer()
