from django.apps import AppConfig
from Core.processQuque import ProcessManager
from HelloWorld.User.apps import SendEmailCodeQueue

class ProcessqueueConfig(AppConfig):
    name = 'HelloWorld.ProcessQueue'


pQueueManager = ProcessManager()
pQueueManager.create_queue("SendEmailCodeQueue", SendEmailCodeQueue)