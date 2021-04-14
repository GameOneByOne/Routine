from abc import ABCMeta,abstractmethod


class Processq(metaclass=ABCMeta):
    def __init__(self, q_name):
        pass

    @abstractmethod
    def push(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def process(self):
        pass

    def state(self):
        pass 
    
    def start(self):
        pass
