from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from HelloWorld.User.models import User
import logging

def HomeView(request):    
    context = {}
    # 用户登陆情况存储在cookies中，所以先判断用户cookies中值的情况
    slug = request.COOKIES.get("slug", "")
    if slug == "":
        context["login_status"] = False
        context["avatar_url"] = "static/image/avatars/avatar_default.png"
        return render(request, 'home.html', context)

    # 这里也要加try，因为有可能用户随便更改了cookies，不能默认slug存在
    try:
        user_info = User.objects.get(slug=slug)
        context["login_status"] = True
        context["avatar_url"] = user_info.avatar_url
        context["user_name"] = user_info.user_name
        context["email"] = user_info.email
    except ObjectDoesNotExist:
        context["login_status"] = False
        context["avatar_url"] = "static/image/avatars/avatar_default.png"

    return render(request, 'home.html', context)

def PdfView(request):
    context = {}
    context["book_slug"] = request.GET.get("bookSlug")
    return render(request, 'viewer.html', context)