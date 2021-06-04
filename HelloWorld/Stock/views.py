from rest_framework.views import APIView
from HelloWorld.Stock.models import Stock, StockSerializer
from HelloWorld.User.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from Core.encrypt import generate_slug
import time
from HelloWorld.settings import * 
from HelloWorld.settings import logger as log
from HelloWorld.ProcessQueue.apps import pQueueManager
import random


# Create your views here.
class StockInfo(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # 如果是获取某本知识库
        if kwargs.get("slug", "") != "":
            try:
                return JsonResponse({"errorCode": 0, "data":StockSerializer(Stock.objects.get(slug=request.GET["slug"])).data}, safe=False, status=200)

            except ObjectDoesNotExist:
                return JsonResponse({"errorCode": 1, "desc": "你要查看的这个知识库不存在哦！"}, safe=False, status=200)

        return JsonResponse({"errorCode": 0, "data":StockSerializer(Stock.objects.all(), many=True).data}, safe=False, status=200)

    def post(self, request, *args, **kwargs):
        # 获取请求数据，并生成对应slug
        stock_name = request.data["name"].strip(" ").strip("\r").strip("\n").strip("\t")
        stock_tag = request.data["name"].strip(" ").strip("\r").strip("\n").strip("\t")
        stock_cover = request.data["cover"]
        stock_desc = request.data["describe"]
        stock_author_slug = request.COOKIES.get("slug")
        stock_author = None
        stock_upgrade_date = time.strftime("%Y-%m-%d", time.localtime())
        stock_slug = generate_slug("Stock", "{}".format(stock_name))
        
        log.info("Stock {}-{} Parse Begin ".format(stock_slug, stock_name))
        # 先检查用户是不是注册用户，可能有爬虫程序之类的
        try:
            stock_author = User.objects.get(slug=stock_author_slug)
        except ObjectDoesNotExist:
            log.warn("User {} Maybe Use Script To Operate Our Site ".format(stock_author_slug))
            return JsonResponse({"errorCode":random.random()}, safe=False, status=200) 
        
        # 之后检查新建的知识库是否与之前的重复
        try:
            Stock.objects.get(slug=stock_slug)
            log.warn("Stock {} Is Already In Database So We Return Error ".format(stock_slug))
            return JsonResponse({"errorCode":1, "desc":"知识库名称重复"}, safe=False, status=200)

        except ObjectDoesNotExist:
            stock = Stock()
            stock.name = stock_name
            stock.author = stock_author
            stock.slug = stock_slug
            stock.upgrade_date = stock_upgrade_date
            stock.cover = stock_cover
            stock.tag = stock_tag
            stock.describe = stock_desc
            stock.save()

            log.info("Stock {}-{} Parse Success".format(stock_slug, stock_name))

            return JsonResponse({"errorCode":0, "desc":"创建成功，前往我的知识库查看或扩展内容"}, safe=False, status=200)
