# rabbitmq_consumer.py
import pika
import json
from log_ingestor_package import crud, database
from log_ingestor_package.schemas import LogEntryCreate


def callback(ch, method, properties, body):
    log_data = json.loads(body)
    
    # Create log entry in the database
    db = database.SessionLocal()
    log = LogEntryCreate(**log_data)
    crud.create_log(db, log)
    
    db.close()

# connection = pika.BlockingConnection(pika.ConnectionParameters(config.settings.RABBITMQ_URL))
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare(queue="logs")

channel.basic_consume(
    queue="logs", on_message_callback=callback, auto_ack=True
)

print("Waiting for logs. To exit press CTRL+C")
channel.start_consuming()
