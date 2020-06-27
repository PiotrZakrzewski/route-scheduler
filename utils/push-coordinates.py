import pika

credentials = pika.PlainCredentials("user", "bitnami")
params = pika.ConnectionParameters("localhost", 5672, credentials=credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue="coordinates")

channel.basic_publish(exchange="", routing_key="coordinates", body="test")
print(" [x] Sent 'Hello World!'")
connection.close()
