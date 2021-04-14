from django.apps import AppConfig
from Core.processQuque import ProcessManager
from HelloWorld.User.apps import SendEmailCodeQueue

class ProcessqueueConfig(AppConfig):
    name = 'ProcessQueue'
