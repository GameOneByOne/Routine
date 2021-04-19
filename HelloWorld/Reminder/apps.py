from django.apps import AppConfig
from Core.processQuque import ProcessQueue
from django_redis import get_redis_connection
from HelloWorld.settings import logger as log


class ReminderConfig(AppConfig):
    name = 'HelloWorld.Reminder'



class RemindMessageQueue(ProcessQueue):
    def __init__(self, q_name):
        super().__init__(q_name)

    def process(self, item):
        redis_conn = get_redis_connection("default")
        redis_conn.lpush(item[0], item[1])