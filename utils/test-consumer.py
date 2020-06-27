import pika

credentials = pika.PlainCredentials("user", "bitnami")
params = pika.ConnectionParameters("localhost", 5672, credentials=credentials)
connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue="results")


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(queue="results", on_message_callback=callback, auto_ack=True)

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
