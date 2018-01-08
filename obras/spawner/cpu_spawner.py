import signal
import sys
import multiprocessing.pool
from functools import partial

from ..worker import Worker
from .abstract_spawner import AbstractSpawner


class CPUSpawner(AbstractSpawner):
    """
    A spawner whose Workers live in independent processes
    """
    def spawn(self):
        """
        Instantiates a Pool of processes and boots a Worker in each
        of them
        """
        pool = Pool(self.n_workers)

        # listen for a SIGINT to be able to terminate the workers
        _kill_pool = partial(self.terminate, pool)
        signal.signal(signal.SIGINT, _kill_pool)

        # boot a Worker on each process of the pool
        pool.map(Worker, [self.conf["worker"] for _ in range(self.n_workers)])

    def terminate(self, pool, _, __):
        pool.terminate()
        sys.exit()


####################################################################
#           non-daemonic multiprocessing pool hack                 #
####################################################################

class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)


class Pool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess

####################################################################

