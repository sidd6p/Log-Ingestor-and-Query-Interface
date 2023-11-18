import pika
import json
from log_ingestor_package import crud, database
from log_ingestor_package.schemas import LogEntryCreate

def callback(ch, method, properties, body):
    db = database.SessionLocal()
    try:
        log_data = json.loads(body)
        log = LogEntryCreate(**log_data)
        crud.create_log(db, log)
        db.commit()  # Commit changes
        print("Log processed and saved to database.")
    except json.JSONDecodeError:
        print("Failed to decode JSON message.")
    except Exception as e:
        print(f"An error occurred: {e}")
        # Here you can decide whether to reject or requeue the message
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    finally:
        db.close()  # Ensure the session is closed

# Setup RabbitMQ connection and channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue="logs")

channel.basic_consume(
    queue="logs", on_message_callback=callback, auto_ack=False
)

print("Waiting for logs. To exit press CTRL+C")
channel.start_consuming()
