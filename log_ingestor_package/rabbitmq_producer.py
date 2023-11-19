# rabbitmq_producer.py
import pika
import json

from log_ingestor_package import config



class RabbitMQProducer:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(config.settings.RABBITMQ_URL)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="logs")

    def publish_log(self, log):
        try:
            self.channel.basic_publish(
                exchange="", routing_key="logs", body=json.dumps(log.dict())
            )
            print("Log successfully published to RabbitMQ.") 
        except (
            pika.exceptions.ConnectionClosedByBroker,
            pika.exceptions.AMQPConnectionError,
        ):
            self.reconnect()
            self.publish_log(log)
        except pika.exceptions.AMQPChannelError as err:
            print(f"Channel error: {err}, stopping...")

    def reconnect(self):
        self.connection.close()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(config.settings.RABBITMQ_URL)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="logs")


rabbitmq_producer = RabbitMQProducer()
