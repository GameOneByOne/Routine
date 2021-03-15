from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from HelloWorld.User.models import User
from django.core.exceptions import ObjectDoesNotExist
from HelloWorld.User.models import UserSerializer
from django.http import JsonResponse
import logging
import json

# Create your views here.
class UserInfo(APIView):
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        account = request.GET.get("account", "")
        password = request.GET.get("password", "")

        content = dict()
        try:
            user_info = User.objects.get(account=account, password=password)
            content = UserSerializer(user_info).data
            content["errorCode"] = 0
            logging.info("Account : {} Request Login In Success".format(account))
        except ObjectDoesNotExist:
            content["errorCode"] = 1
            logging.info("Account : {} , password : {}, Request Login In Error".format(password))

        return JsonResponse(content, status=200)

    def post(self, request, *args, **kwargs):
        account = request.POST.get("account", "")
        password = request.POST.get("password", "")

        content = dict()
        try:
            user_info = User.objects.get(account=account)
            content["errorCode"] = 1
            logging.info("Account : {} Request Sign In Failed".format(account))
        except ObjectDoesNotExist:
            User(account=account, password=password).save()
            content = UserSerializer(User.objects.get(account=account)).data
            content["errorCode"] = 0
            logging.info("Account : {} Request Sign In Success".format(account))

        return JsonResponse(content, status=200)

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