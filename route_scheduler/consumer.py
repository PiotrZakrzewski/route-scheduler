import os
import logging
import time
import pika
from route_scheduler.serializers import deserialize_task, serialize_result
from route_scheduler.scheduler import find_routes
from marshmallow.exceptions import MarshmallowError

log = logging.getLogger("consumer")

RETRY_COOLOFF = 3


def connect_with_retry():
    mq_usr = os.getenv("MQ_USERNAME", "user")
    mq_pwd = os.getenv("MQ_PWD", "bitnami")
    mq_host = os.getenv("MQ_HOST", "localhost")
    mq_port = int(os.getenv("MQ_PORT", "5672"))
    credentials = pika.PlainCredentials(mq_usr, mq_pwd)
    params = pika.ConnectionParameters(mq_host, mq_port, credentials=credentials)
    while True:
        try:
            connection = pika.BlockingConnection(params)
        except pika.exceptions.AMQPConnectionError:
            log.warn(
                "Could not connect to RabbitMQ, will retry in {} sec...".format(
                    RETRY_COOLOFF
                )
            )
            time.sleep(RETRY_COOLOFF)
            continue
        return connection


def start_consuming():
    connection = connect_with_retry()
    channel = connection.channel()

    def callback(ch, method, properties, body):
        try:
            task = deserialize_task(body)
        except MarshmallowError:
            log.error("Invalid task %s", body)
            return
        coordinates, start = task["coordinates"], task["start"]
        cars, t_id = task["cars"], task["tid"]
        route = find_routes(coordinates, start, cars)
        if not route:
            log.error("Could not find any route for %s", task)
            return
        msg = serialize_result(route, t_id)
        channel.basic_publish(exchange="", routing_key="results", body=msg)

    channel.queue_declare(queue="coordinates")
    channel.queue_declare(queue="results")
    channel.basic_consume(
        queue="coordinates", on_message_callback=callback, auto_ack=True
    )
    channel.start_consuming()
