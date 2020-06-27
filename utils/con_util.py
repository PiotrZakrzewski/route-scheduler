import os
import time
import pika

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
            print(
                "Could not connect to RabbitMQ, will retry in {} sec...".format(
                    RETRY_COOLOFF
                )
            )
            time.sleep(RETRY_COOLOFF)
            continue
        return connection
