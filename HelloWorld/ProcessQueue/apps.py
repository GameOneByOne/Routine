from django.apps import AppConfig
from Core.processQuque import ProcessManager
from HelloWorld.User.apps import SendEmailCodeQueue
from HelloWorld.Book.apps import ProcessBookQueue
from HelloWorld.Reminder.apps import RemindMessageQueue

class ProcessqueueConfig(AppConfig):
    name = 'HelloWorld.ProcessQueue'


pQueueManager = ProcessManager()
pQueueManager.create_queue("SendEmailCodeQueue", SendEmailCodeQueue)
pQueueManager.create_queue("ProcessBookQueue", ProcessBookQueue)
pQueueManager.create_queue("RemindMessageQueue", RemindMessageQueue)