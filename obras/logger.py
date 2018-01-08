import redis


class Logger:
    """
    Log stuff to a Redis pubsub
    """
    def __init__(self, conf, channel):
        self.redis = redis.Redis(**conf)
        self.channel = channel

    def log(self, msg):
        self.redis.publish(self.channel, msg)
