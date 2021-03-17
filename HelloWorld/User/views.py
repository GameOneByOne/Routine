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
        email = request.GET.get("email", "")
        password = request.GET.get("password", "")

        content = dict()
        try:
            user_info = User.objects.get(email=email, password=password)
            content = UserSerializer(user_info).data
            content["errorCode"] = 0
            logging.info("Email : {} Request Login In Success".format(email))
        except ObjectDoesNotExist:
            content["errorCode"] = 1
            logging.info("Email : {} , password : {}, Request Login In Error".format(email, password))

        return JsonResponse(content, status=200)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email", "")

        content = dict()
        try:
            user_info = User.objects.get(email=email)
            content["errorCode"] = 1
            logging.info("Email : {} Request Sign In Failed".format(email))
        except ObjectDoesNotExist:
            user = UserSerializer(data=request.POST)
            if user.is_valid():
                user.save()
                content = UserSerializer(User.objects.get(email=email)).data
                content["errorCode"] = 0
                logging.info("Email : {} Request Sign In Success".format(email))
            else:
                content["errorCode"] = 1
                logging.info("Email : {} Request Sign In Filed Because Of Invaild Format".format(email))
                
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