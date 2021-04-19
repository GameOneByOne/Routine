from rest_framework.views import APIView
from django.http import JsonResponse
from django_redis import get_redis_connection
from HelloWorld.settings import logger as log
import re


# Create your views here.
class ReminderInfo(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        key = request.COOKIES.get("csrftoken", "")
        if key == "": return JsonResponse({"errorCode": 1}, status=200)

        redis_conn = get_redis_connection("default")
        remind_msg = redis_conn.lpop(key)

        if remind_msg:
            remind_msg = remind_msg.decode("utf-8")
            msg_result = re.search("\[warn\]|\[info\]|\[error\]", remind_msg)
            msg_type, msg_span = msg_result.group(), msg_result.span()
            return JsonResponse({"errorCode": 0, "desc":remind_msg[msg_span[-1]:], "msg_type":msg_type}, status=200)

        return JsonResponse({"errorCode": 1}, status=200)

    def post(self, request, *args, **kwargs):
        pass