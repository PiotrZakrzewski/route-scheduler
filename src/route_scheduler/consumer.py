import os
import pika
from route_scheduler.serializers import deserialize_task, serialize_result
from route_scheduler.scheduler import find_routes


def start_consuming():
    mq_usr = os.getenv("MQ_USERNAME", "user")
    mq_pwd = os.getenv("MQ_PWD", "bitnami")
    mq_host = os.getenv("MQ_HOST", "localhost")
    mq_port = int(os.getenv("MQ_PORT", "5672"))
    credentials = pika.PlainCredentials(mq_usr, mq_pwd)
    params = pika.ConnectionParameters(mq_host, mq_port, credentials=credentials)
    connection = pika.BlockingConnection(params)

    channel = connection.channel()

    def callback(ch, method, properties, body):
        task = deserialize_task(body)
        coordinates, start, cars = task["coordinates"], task["start"], task["cars"]
        route = find_routes(coordinates, start, cars)
        msg = serialize_result(route)
        channel.basic_publish(exchange="", routing_key="results", body=msg)

    channel.queue_declare(queue="coordinates")
    channel.queue_declare(queue="results")
    channel.basic_consume(
        queue="coordinates", on_message_callback=callback, auto_ack=True
    )
    channel.start_consuming()
