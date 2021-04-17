from rest_framework.views import APIView
from HelloWorld.User.models import User, UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from Core.email import is_email
from django_redis import get_redis_connection
from Core.encrypt import md5
from HelloWorld.settings import logger as log
from HelloWorld.ProcessQueue.apps import pQueueManager

# Create your views here.
class UserInfo(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        email = request.GET.get("email", "")
        password = request.GET.get("password", "")

        try:
            user_info = User.objects.get(email=email, password=md5(password))
            content = UserSerializer(user_info).data
            content["errorCode"] = 0
            log.info("Email : {} Request Login In Success".format(email))
            return JsonResponse(content, status=200)

        except ObjectDoesNotExist:
            log.info("Email : {} , password : {}, Request Login In Error".format(email, password))
            return JsonResponse({"errorCode": 1, "desc":"诶呀!! 不明入侵者!!"}, status=200)        

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email", "")

        try:
            user_info = User.objects.get(email=email)
            log.info("Email : {} Request Sign Up Failed, Because Signed Already".format(email))
            return JsonResponse({"errorCode": 1, "desc": "欸? 这个邮箱已经注册过啦，你是邮箱本人还是不明觉厉的黑客？"}, status=200)

        except ObjectDoesNotExist:
            user = UserSerializer(data=request.POST)
            
            if user.is_valid():
                user.save()
                content = UserSerializer(User.objects.get(email=email)).data
                content["errorCode"] = 0
                log.info("Email : {} Request Sign Up Success".format(email))
                return JsonResponse(content, status=200)

            else:
                log.info("Email : {} Request Sign Up Failed Because Of {}".format(email, user.errors))
                return JsonResponse({"errorCode": 1, "desc": "由于宇宙射线原因, 本次注册失败了, 请等管理员修复..."}, status=200)

    def patch(self, request, *args, **kwargs):
        slug = request.POST.get("slug", "")
        user_ins = User.objects.get(slug=slug)
        user = UserSerializer(user_ins, data=request.POST)
        if user.is_valid():
            user.save()
            return JsonResponse({"errorCode": 0, "desc": "你的信息已经更新了哦～～"}, status=200)

        return JsonResponse({"errorCode": 1, "desc": "诶～有错误产生啦，得找管理员查查"}, status=200)

class EmailCode(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        email = request.GET.get("email", "")
        log.info("Email: {} Acquire Sign Up Random Code".format(email))
        if is_email(email): 
            redis_conn = get_redis_connection("default")

            # 先检查之前有没有发过
            remain_time = redis_conn.ttl(email)
            if remain_time <= 0:
                pQueueManager.push("SendEmailCodeQueue", email)
                return JsonResponse({"errorCode": 0, "desc": "验证码已经上路~~"}, status=200)
            else:
                return JsonResponse({"errorCode": 1, "desc": "拜托..验证码已经发过啦, {} 秒后，再来呗".format(remain_time)}, status=200)

        return JsonResponse({"errorCode": 1, "desc": "诶..邮箱格式好像不对, 检查一下呗"}, status=200)

    def post(self, request, *args, **kwargs):
        code = request.data.get("code", "")
        email = request.data.get("email", "")
        
        redis_conn = get_redis_connection("default")
        pre_code = redis_conn.get(email)

        if pre_code and code == pre_code.decode("utf-8"):
            return JsonResponse({"errorCode": 0}, status=200) 
            
        return JsonResponse({"errorCode": 1, "desc": "嘿..验证码输错啦, 再试一下, 加油！"}, status=200)
