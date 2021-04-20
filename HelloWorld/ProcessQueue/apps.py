from django.apps import AppConfig
from Core.processQuque import ProcessManager
from HelloWorld.User.apps import SendEmailCodeQueue
from HelloWorld.Book.apps import ProcessBookQueue
from HelloWorld.Reminder.apps import RemindMessageQueue

class ProcessqueueConfig(AppConfig):
    name = 'HelloWorld.ProcessQueue'


"""
异步处理队列管理器，主要用于某些异步处理的场景，加快请求的返回，资源的释放等等
"""
pQueueManager = ProcessManager()

# 注册邮箱验证码的发送队列
pQueueManager.create_queue("SendEmailCodeQueue", SendEmailCodeQueue)

# PDF文件的后台处理队列
pQueueManager.create_queue("ProcessBookQueue", ProcessBookQueue)

# 消息提醒器的推送度列
pQueueManager.create_queue("RemindMessageQueue", RemindMessageQueue)