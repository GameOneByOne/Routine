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
    
    # 先获取当前用户信息
    account = request.GET.get("account")
    password = request.GET.get("password")
    user_info = User.objects.get(account=account, password=password)

    context["avatar_url"] = user_info.avatar_url
    context["user_name"] = user_info.user_name
    context["birthday"] = user_info.birthday
    context["email"] = user_info.email

    return render(request, 'home.html', context)

def PdfView(request):
    context = {}
    context["book_slug"] = request.GET.get("bookSlug")
    return render(request, 'viewer.html', context)