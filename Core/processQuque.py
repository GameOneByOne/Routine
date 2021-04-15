from abc import ABCMeta,abstractmethod
from Core.metaclass import SingletonType
from queue import Queue
from logging import log
from threading import Thread
import time

class ProcessManager(metaclass=SingletonType):
    def __init__(self):
        self.queue_map = {}

    def create_queue(self, q_name, cls):
        if q_name in self.queue_map.keys(): return -1
        p_queue = cls(q_name)
        self.queue_map[q_name] = p_queue
        p_queue.daemon = False
        # print(1111111111)
        p_queue.start()
        # print(1111111111)

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

        self.wait_queue.put(args[0])

    def stat(self):
        log.info("[ ProcessQueue ] Queue {} Routine Report , Current Size: {}, Done Size: {}".format(self.queue_name, self.queue_name.qsize(), self.done_count))

    def run(self):
        while (True):
            if (not self.wait_queue.empty()):
                try:
                    self.process(self.wait_queue.get())
                except Exception as e:
                    log.error("[ ProcessQueue ] Our Queue {} Is Error When We Process, MayBe You Should Have A Look !".format(self.queue_name))

            else:
                time.sleep(1)
