from rest_framework.views import APIView
from django.http import JsonResponse
from django_redis import get_redis_connection
from HelloWorld.settings import logger as log
import re


# Create your views here.
class ReminderInfo(APIView):
    """
    提醒器，用于用户和后台的沟通，其中
    GET方法是由后台发往用户的消息，
    POST方法是用户放给后台的消息
    """
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # 这里默认只给认证过的用户推送消息
        key = request.COOKIES.get("csrftoken", "")
        if key == "": return JsonResponse({"errorCode": 1}, status=200)

        # 使用redis获取对应key的缓存消息队列
        redis_conn = get_redis_connection("default")
        remind_msg = redis_conn.lpop(key)

        if remind_msg:
            # 如果有消息，则这里需要进行消息类型的判断，以方便web上展示不同类型的消息
            remind_msg = remind_msg.decode("utf-8")
            msg_result = re.search("\[warn\]|\[info\]|\[error\]", remind_msg)
            msg_type, msg_span = msg_result.group(), msg_result.span()
            return JsonResponse({"errorCode": 0, "desc":remind_msg[msg_span[-1]:], "msg_type":msg_type}, status=200)

        return JsonResponse({"errorCode": 1}, status=200)

    def post(self, request, *args, **kwargs):
        # 获取头部中的消息，并打印在日志中
        message = request.POST.get("message", "")
        log.info("[ ReminderInfo ] We Receive A Message : {}".format(message))

