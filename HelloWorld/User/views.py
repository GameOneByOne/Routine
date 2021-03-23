from rest_framework.views import APIView
from HelloWorld.User.models import User, UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django_redis import get_redis_connection
from Core.email import send_sign_up_email, is_email
from HelloWorld.settings import logger as log

# Create your views here.
class UserInfo(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        email = request.GET.get("email", "")
        password = request.GET.get("password", "")

        try:
            user_info = User.objects.get(email=email, password=password)
            content = UserSerializer(user_info).data
            log.info("Email : {} Request Login In Success".format(email))
            return JsonResponse({"errorCode": 0}, status=200)

        except ObjectDoesNotExist:
            log.info("Email : {} , password : {}, Request Login In Error".format(email, password))
            return JsonResponse({"errorCode": 1, "desc":"Your Email Or Password Is Worry, Please Check."}, status=200)        

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email", "")

        try:
            user_info = User.objects.get(email=email)
            log.info("Email : {} Request Sign Up Failed, Because Signed Already".format(email))
            return JsonResponse({"errorCode": 1, "desc": "The Email Have Signed Already, Did You Forget Your Password?"}, status=200)

        except ObjectDoesNotExist:
            user = UserSerializer(data=request.POST)
            if user.is_valid():
                user.save()
                content = UserSerializer(User.objects.get(email=email)).data
                content["errorCode"] = 0
                log.info("Email : {} Request Sign Up Success".format(email))
                return JsonResponse(content, status=200)

            else:
                log.info("Email : {} Request Sign Up Filed Because Of {}".format(email, user.errors))
                return JsonResponse({"errorCode": 1, "desc": "Sign Up Failed, Please Call The Web Manager"}, status=200)
                
    def patch(self, request, *args, **kwargs):
        data = {
            'data': 'patch success'
        }
        return JsonResponse(data, status=200)

    def delete(self, request, *args, **kwargs):
        data = {
            'data': 'delete success'
        }
        return JsonResponse(data, status=200)


class EmailCode(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        email = request.GET.get("email", "")
        log.info("email: {} Acquire Sign Up Random Code".format(email))
        if is_email(email): 
            redis_conn = get_redis_connection("default")

            # 先检查之前有没有发过
            remain_time = redis_conn.ttl(email)
            if remain_time <= 0:
                code = send_sign_up_email(email)

                if code:
                    redis_conn.set(email, code, ex=60)
                    return JsonResponse({"errorCode": 0, "desc": "Varify Email Had Sent"}, status=200)

                else:
                    return JsonResponse({"errorCode": 1, "desc": "Your Email Is Not Exist.."}, status=200)

            else:
                return JsonResponse({"errorCode": 1, "desc": "Try Again? Please Hold On {} Seconds".format(remain_time)}, status=200)

        return JsonResponse({"errorCode": 1, "desc": "Your Email's Format Is Worry, Please Check."}, status=200)

    def post(self, request, *args, **kwargs):
        code = request.data.get("code", "")
        email = request.data.get("email", "")
        
        redis_conn = get_redis_connection("default")
        pre_code = redis_conn.get(email)

        if pre_code and code == pre_code.decode("utf-8"):
            return JsonResponse({"errorCode": 0}, status=200) 
        return JsonResponse({"errorCode": 1, "desc": "Code Varify Error. Did You Input The Correct Code?"}, status=200) 
