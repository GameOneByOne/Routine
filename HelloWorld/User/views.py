from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from HelloWorld.User.models import User
from Core.encrypt import md5, generate_slug
from django.core.exceptions import ObjectDoesNotExist
import json

# Create your views here.
class UserInfo(APIView):
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        account = request.GET.get("account", "")
        password = request.GET.get("password", "")

        try:
            user_info = User.objects.get(account=account, password=password)
        except ObjectDoesNotExist:
            return Response({"errorCode": 1}, status=200)

        return Response({"errorCode": 0, "UserInfo":str(user_info)}, status=200)

    def post(self, request, *args, **kwargs):
        req_data = json.loads(request.body.decode("utf-8"))
        account = req_data.get("account", "")
        password = req_data.get("password", "")

        try:
            user_info = User.objects.get(account=account)
        except ObjectDoesNotExist:
            User(account=account, password=password).save()
            return Response({"errorCode": 0}, status=200)

        return Response({"errorCode": 1}, status=200)

    def patch(self, request, *args, **kwargs):
        data = {
            'data': 'patch success'
        }
        return Response(data, status=200)

    def delete(self, request, *args, **kwargs):
        data = {
            'data': 'delete success'
        }
        return Response(data, status=200)