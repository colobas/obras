class AbstractSpawner:
    """
    Spawner of workers. Because the workers might be of different natures,
    there have to be different spawners
    """
    def __init__(self, conf):
        self.conf = conf
        self.n_workers = conf["n_workers"]

    def spawn(self):
        pass

    def terminate(self, *args):
        pass
