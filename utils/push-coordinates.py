import pika
import json
import random
from con_util import connect_with_retry


connection = connect_with_retry()
channel = connection.channel()
channel.queue_declare(queue="coordinates")
random_cords = [(random.randint(0, 1000), random.randint(0, 1000)) for _ in range(10)]

task = {"coordinates": [(0, 1), (1, 0)], "start": 0, "cars": 1, "tid": 1337}
big_task = {"coordinates": random_cords, "start": 0, "cars": 1, "tid": 7331}


def push(task):
    channel.basic_publish(exchange="", routing_key="coordinates", body=json.dumps(task))
    print(" [x] Sent {}".format(task))


push(task)
push(big_task)
connection.close()
