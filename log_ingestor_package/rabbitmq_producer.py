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
        try:
            self.channel.basic_publish(
                exchange="", routing_key="logs", body=json.dumps(log.dict())
            )
        except pika.exceptions.ConnectionClosedByBroker:
            # Attempt to reconnect and then republish
            self.reconnect()
            self.publish_log(log)
        except pika.exceptions.AMQPChannelError as err:
            print(f"Channel error: {err}, stopping...")
            # Add more robust error handling here
        except pika.exceptions.AMQPConnectionError:
            print("Connection was closed, retrying...")
            # Attempt to reconnect and then republish
            self.reconnect()
            self.publish_log(log)

    def reconnect(self):
        # Close existing connection
        self.connection.close()
        # Create a new connection
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="logs")

rabbitmq_producer = RabbitMQProducer()
