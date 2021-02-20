from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from HelloWorld.User.models import User
import logging


def LoginView(request):    
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'login.html', context)

def HomeView(request):    
    context = {}
    context['hello'] = 'Hello World!'
    
    account = request.GET.get("account")
    password = request.GET.get("password")
    user_info = User.objects.get(account=account, password=password)

    context["avatar_url"] = user_info.avatar_url

    return render(request, 'home.html', context)