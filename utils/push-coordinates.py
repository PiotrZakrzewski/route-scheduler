import pika
import json


credentials = pika.PlainCredentials("user", "bitnami")
params = pika.ConnectionParameters("localhost", 5672, credentials=credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue="coordinates")


task = {"coordinates": [(0, 1), (1, 0)], "start": 0, "cars": 1}

channel.basic_publish(exchange="", routing_key="coordinates", body=json.dumps(task))
print(" [x] Sent {}".format(task))
connection.close()
