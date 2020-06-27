import pika
from con_util import connect_with_retry


connection = connect_with_retry()

channel = connection.channel()

channel.queue_declare(queue="results")


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(queue="results", on_message_callback=callback, auto_ack=True)

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
