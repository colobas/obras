import time
import pika
import json
from .logger import Logger


class Manager:
    """
    Enqueues Tasks on a work queue - implemented in RabbitMQ
    """
    def __init__(self, conf):
        # timestamp and id creation
        self.date = time.time()
        self.id = "MAN"+str(hash(str(self.date)+str(id(self))) & 0xffffffffffffffff)

        # rabbitmq setup
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(**conf["rabbitmq"]["connection_parameters"]))
        self._channel = self._connection.channel()
        self._channel.queue_declare(**conf["rabbitmq"]["queue_declare"])

        # redis pubsub setup
        self.logger = Logger(conf["logger"], "um_canal")
        self.conf = conf

    def deploy(self, job_conf):
        """
        Enqueue a list of tasks on the work queue
        :param job_conf: configuration params and task metadata
        """
        for task in job_conf["tasks"]:
            self.logger.log("[{}] {} added task {} to queue".format(time.time(),
                                                                    self.id, task["type"]))

            # the common_payload contains metadata that's relevant to all the tasks
            # but it isn't placed inside each task's payload on the config file to avoid
            # repetition. it's copied here to each task's payload for that reason
            task["common_payload"] = job_conf["common_payload"]
            self._enqueue(task)

        self._connection.close()

    def _enqueue(self, task):
        """
        Enqueue a task on the work queue
        :param task:
        """
        self._channel.basic_publish(
            exchange="",
            routing_key="task_queue",
            body=json.dumps(task),
            properties=pika.BasicProperties(
               delivery_mode=2
            )
        )
