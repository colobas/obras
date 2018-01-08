from .abstract_recipe import AbstractRecipe
import time
import os


class SpendTimeRecipe(AbstractRecipe):
    """
    Dummy task that simply sleeps 10 seconds and logs a simple message
    """
    def _execute(self):
        self.logger.log("[{}] worker {} will sleep 2 seconds for {}".format(
            time.time(), self.get_worker_id(), self.get_task_id()
        ))

        time.sleep(2)

        self.logger.log("[{}] worker {} slept 2 seconds for {}".format(
            time.time(), self.get_worker_id(), self.get_task_id()
        ))

