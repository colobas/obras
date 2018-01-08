import time

from ..logger import Logger
from ..manager import Manager
from ..utils import load_config


class AbstractRecipe:
    """
    Defines a set of instructions that will constitute a Task
    """
    def __init__(self, metadata):
        """
        Initialization of the Recipe
        :param metadata: relevant data needed to configure and run this Recipe
        """

        self.metadata = metadata
        self.logger = Logger(metadata["common_payload"]["logger"], "um_canal")
        self.date = time.time()
        self.id = "TASK"+str(hash(str(self.date)+str(id(self))) & 0xffffffffffffffff)

    def _execute(self):
        """
        Concrete Recipes should implement this method
        """
        raise NotImplemented

    def _callbacks(self):
        """
        Enqueues new Tasks that should only be executed after this one
        """
        if "tasks" in self.metadata["payload"]:
            conf = load_config("./config/example_manager.conf")
            manager = Manager(conf)
            new_conf = {
                "common_payload" : self.metadata["common_payload"],
                "tasks" : self.metadata["payload"]["tasks"]
            }
            manager.deploy(new_conf)

    def get_worker_id(self):
        return self.metadata["common_payload"]["worker_id"]

    def get_task_id(self):
        return self.id

    def __call__(self):
        self._execute()
        self._callbacks()
