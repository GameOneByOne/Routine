from django.apps import AppConfig
from Core.processQuque import ProcessQueue


class UserConfig(AppConfig):
    name = 'User'


class SendEmailCodeQueue(ProcessQueue):
    def __init__(self, q_name):
        super().__init__(q_name)
    
    def process(self, item):
        print(11)

