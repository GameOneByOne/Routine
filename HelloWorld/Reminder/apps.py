from django.apps import AppConfig
from Core.processQuque import ProcessQueue
from django_redis import get_redis_connection
from HelloWorld.settings import logger as log


class ReminderConfig(AppConfig):
    name = 'HelloWorld.Reminder'



class RemindMessageQueue(ProcessQueue):
    """
    消息提醒器队列，异步的完成消息的推送
    """
    def __init__(self, q_name):
        super().__init__(q_name)

    def process(self, item):
        # 获取redis链接，并判断如果目标用户的key为空，表示是未验证过的用户，则直接返回，不做推送
        redis_conn = get_redis_connection("default")
        if item[0] == "": return 
        
        # 消息入缓存
        redis_conn.lpush(item[0], item[1])