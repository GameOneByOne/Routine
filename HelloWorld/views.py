from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.shortcuts import render
from HelloWorld.User.models import User
from HelloWorld.Stock.models import Stock, Piece, PieceInfoSerializer, PieceContentForEditSerializer
from HelloWorld.settings import logger as log 

def HomeView(request, *args, **kwargs):    
    context = {}
    # 用户登陆情况存储在cookies中，所以先判断用户cookies中值的情况
    slug = request.COOKIES.get("slug", "")
    if slug == "":
        context["login_status"] = False
        context["user_name"] = "未登陆"
        context["avatar_id"] = "ahf64532a2124a1231"
        return render(request, 'home.html', context)

    # 这里也要加try，因为有可能用户随便更改了cookies，不能默认slug存在
    try:
        user_info = User.objects.get(slug=slug)
        context["login_status"] = True
        context["avatar_id"] = user_info.avatar_id
        context["user_name"] = user_info.user_name
        context["email"] = user_info.email
        
    except ObjectDoesNotExist:
        context["login_status"] = False
        context["avatar_id"] = "ahf64532a2124a1231"

    return render(request, 'home.html', context)

def MdReadView(request, *args, **kwargs):
    context = {}
    # 还是需要拿到Stock的Name作为显示的
    stock = None
    try:
        stock = Stock.objects.get(slug=kwargs.get("slug", ""))
        context["stock_name"] = stock.name
    except ObjectDoesNotExist:
        return render(request, 'viewer.html', context)

    # 之后再先获取所有Piece的内容，之后在Html中的Js进行分批加载
    pieces = PieceInfoSerializer(Piece.objects.filter(belong_stock=stock).order_by("index"), many=True).data
    
    context["pieces"] = list()
    ind = 1
    for piece in pieces:
        context["pieces"].append({"name": piece["name"].split(".")[0], "slug":piece["slug"], "path":piece["content"]})
        ind += 1
        
    return render(request, 'viewer.html', context)

def MdEditView(request, *args, **kwargs):
    context = {}
    try:
        piece = Piece.objects.get(slug=kwargs.get("slug", ""))
        context = PieceContentForEditSerializer(piece).data
    except ObjectDoesNotExist:
        return render(request, 'editer.html', context)

    return render(request, 'editer.html', context)
