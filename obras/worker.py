import time
import pika
import json
from .logger import Logger


class Worker:
    """
    Listens on the queue and performs tasks
    """
    def __init__(self, conf):
        self.id = "WORKER"+str(hash(str(time.time())+str(id(self))) & 0xffffffffffffffff)

        # logger setup
        self.logger = Logger(conf["logger"], "um_canal")
        self.logger.log("[{}] Booted worker {}".format(time.time(), self.id))

        # rabbitmq setup
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(**conf["rabbitmq"]["connection_parameters"]))
        self._channel = self._connection.channel()
        self._channel.queue_declare(**conf["rabbitmq"]["queue_declare"])
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(self._do_work, queue="task_queue")

        self._channel.start_consuming()

    def _do_work(self, ch, method, properties, payload):
        # deserialize payload
        payload = json.loads(payload)

        # import class that describes the task to execute
        recipe = dynamic_import(payload["type"])

        # pass the ID of the worker that picked the task up
        payload["common_payload"]["worker_id"] = self.id

        # instantiate, pass the metadata and call it
        recipe(payload)()

        ch.basic_ack(delivery_tag=method.delivery_tag)


def dynamic_import(name):
    """
    Helper function to dynamically import recipes to be executed
    :param name: recipe class name
    :return: the class
    """
    mod = __import__("obras.recipe", globals(), locals(), [name], 0)
    return getattr(mod, name)


