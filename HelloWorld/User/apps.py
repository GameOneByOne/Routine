from django.apps import AppConfig
from Core.processQuque import ProcessQueue
from Core.email import send_email
from django_redis import get_redis_connection
import time

class UserConfig(AppConfig):
    name = 'HelloWorld.User'


class SendEmailCodeQueue(ProcessQueue):
    def __init__(self, q_name):
        super().__init__(q_name)
    
    def process(self, item):
        random_code = str(time.time()).split(".")[-1]
        message = """
            <h3>Welcome Friend<h3>
            <p>&nbsp;&nbsp;&nbsp;&nbsp; We are gald about received your sign up request, your verify code is {} <p>
        """.format(random_code)

        if send_email(item, message):
            redis_conn = get_redis_connection("default")
            redis_conn.set(item, random_code, ex=60)

        return 

