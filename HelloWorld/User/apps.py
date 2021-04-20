from django.apps import AppConfig
from Core.processQuque import ProcessQueue
from Core.email import send_email
from django_redis import get_redis_connection
import time

class UserConfig(AppConfig):
    name = 'HelloWorld.User'


class SendEmailCodeQueue(ProcessQueue):
    """
    注册邮箱发送验证码的发送队列，主要是为了让请求快速的返回，因为有时候发邮件太慢啦
    """
    def __init__(self, q_name):
        super().__init__(q_name)
    
    def process(self, item):
        # 先获取一下验证码，时间戳的小数部分， 消息也是这里写死的
        random_code = str(time.time()).split(".")[-1]
        message = """
            <h3>Welcome Friend<h3>
            <p>&nbsp;&nbsp;&nbsp;&nbsp; We are gald about received your sign up request, your verify code is {} <p>
        """.format(random_code)

        # 发送邮件，并记录邮箱和验证码的映射缓存
        if send_email(item, message):
            redis_conn = get_redis_connection("default")
            redis_conn.set(item, random_code, ex=60)

        return 

