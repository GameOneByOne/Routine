from abc import ABCMeta,abstractmethod
from Core.metaclass import SingletonType
from queue import Queue
from threading import Thread
import time
from HelloWorld.settings import logger as log


class ProcessManager(metaclass=SingletonType):
    def __init__(self):
        self.queue_map = {}

    def create_queue(self, q_name, cls):
        if q_name in self.queue_map.keys(): return 
        p_queue = cls(q_name)
        self.queue_map[q_name] = p_queue
        p_queue.daemon = False
        p_queue.start()

    def push(self, q_name, *args):
        self.queue_map[q_name].push(*args)

    def routine_stat(self, q_name, *args):
        pass


class ProcessQueue(Thread, metaclass=ABCMeta):
    def __init__(self, q_name):
        super().__init__()
        self.queue_name = q_name;
        self.wait_queue = Queue(maxsize=50)
        self.done_count = 0;

    @abstractmethod
    def process(self, item):
        pass

    def push(self, *args):
        if (self.wait_queue.full()):
            log.warn("[ ProcessQueue ] Our Queue {} Is Full, MayBe We Have Some Trouble !".format(self.queue_name))
            return 

        log.debug("[ ProcessQueue ] A New Item Push Into Our Queue {} ".format(self.queue_name))
        self.wait_queue.put(args[0])

    def stat(self):
        log.info("[ ProcessQueue ] Queue {} Routine Report , Current Size: {}, Done Size: {}".format(self.queue_name, self.queue_name.qsize(), self.done_count))

    def run(self):
        while (True):
            if (not self.wait_queue.empty()):
                try:
                    self.process(self.wait_queue.get())
                    log.debug("[ ProcessQueue ] Our Queue {} Completed A Item".format(self.queue_name))
                except Exception as e:
                    log.error("[ ProcessQueue ] Our Queue {} Is Error When We Process, MayBe You Should Have A Look ! {}".format(self.queue_name, e))

            else:
                time.sleep(1)
