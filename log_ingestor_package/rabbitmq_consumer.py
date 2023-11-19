# rabbitmq_consumer.py
import pika
import json
from log_ingestor_package import crud, database
from log_ingestor_package.schemas import LogEntry

from log_ingestor_package import config


def callback(ch, method, properties, body):
    db = database.SessionLocal()
    try:
        log_data = json.loads(body)
        log = LogEntry(**log_data, metadata=log_data['meta_data'])
        crud.create_log(db, log)
        db.commit()
        ch.basic_ack(
            delivery_tag=method.delivery_tag
        )  # Acknowledge after successful processing
        print("Log successfully consumed and processed.") 
    except Exception as e:
        print(f"An error occurred: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)  # Reject the message on error
    finally:
        db.close()


# RabbitMQ setup and consumption
connection = pika.BlockingConnection(pika.ConnectionParameters(config.settings.RABBITMQ_URL))
channel = connection.channel()
channel.queue_declare(queue="logs")
channel.basic_consume(queue="logs", on_message_callback=callback, auto_ack=False)
print("Waiting for logs. To exit press CTRL+C")
channel.start_consuming()
