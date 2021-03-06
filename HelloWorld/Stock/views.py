from rest_framework.views import APIView
from HelloWorld.Stock.models import Stock, Piece, StockSerializer, PieceInfoSerializer, PieceContentForReadSerializer
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
        if request.GET.get("userSlug", "") != "":
            # 先看用户在不在
            user = None
            try:
                user = User.objects.get(slug=request.GET.get("userSlug", ""))
            except ObjectDoesNotExist:
                return JsonResponse({"errorCode": 1, "desc": "你还未登陆哦！"}, safe=False, status=200)
                
            return JsonResponse({"errorCode": 0, "data":StockSerializer(Stock.objects.filter(author=user), many=True).data}, safe=False, status=200)

        return JsonResponse({"errorCode": 0, "data":StockSerializer(Stock.objects.all(), many=True).data}, safe=False, status=200)

    def post(self, request, *args, **kwargs):
        # 获取请求数据，并生成对应slug
        stock_name = request.data["name"].strip(" ").strip("\r").strip("\n").strip("\t")
        stock_tag = request.data["tag"].strip(" ").strip("\r").strip("\n").strip("\t")
        stock_cover = request.data["cover"]
        stock_desc = request.data["describe"]
        stock_author_slug = request.COOKIES.get("slug", "")
        stock_author = None
        stock_upgrade_date = time.strftime("%Y-%m-%d", time.localtime())
        stock_slug = generate_slug("Stock", "{}".format(stock_name))
        
        log.info("Stock {}-{} Parse Begin ".format(stock_slug, stock_name))
        # 先检查用户是不是注册用户，可能有爬虫程序之类的
        try:
            stock_author = User.objects.get(slug=stock_author_slug)
        except ObjectDoesNotExist:
            log.warn("User {} Maybe Use Script To Operate Our Site ".format(stock_author_slug))
            return JsonResponse({"errorCode":random.random(), "desc": "你需要先登陆之后在创建自己的知识库！"}, safe=False, status=200) 
        
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

    def patch(self, request, *args, **kwargs):
        # 获取请求数据，并生成对应slug
        stock_name = request.data["name"].strip(" ").strip("\r").strip("\n").strip("\t")
        stock_tag = request.data["tag"].strip(" ").strip("\r").strip("\n").strip("\t")
        stock_desc = request.data["describe"]
        stock_slug = request.data["slug"]
        stock_author_slug = request.COOKIES.get("slug")
        stock_pieces = request.data["pieces"]
        
        log.info("Stock {}-{} Patch Request ".format(stock_slug, stock_name))
        # 先检查用户是不是注册用户，可能有爬虫程序之类的
        try:
            User.objects.get(slug=stock_author_slug)
        except ObjectDoesNotExist:
            log.warn("User {} Maybe Use Script To Operate Our Site ".format(stock_author_slug))
            return JsonResponse({"errorCode":random.random()}, safe=False, status=200) 
        
        # 先更新Stock
        try:
            stock = Stock.objects.get(slug=stock_slug)
            stock.name = stock_name
            stock.tag = stock_tag
            stock.describe = stock_desc
            if request.data.get("cover", "") != "": stock.cover = request.data["cover"]

            stock.save()
            log.info("Stock {}-{} Parse Success".format(stock_slug, stock_name))

        except ObjectDoesNotExist:
            log.warn("Stock {} Is Not In Database So We Return Error ".format(stock_slug))
            return JsonResponse({"errorCode":1, "desc":"知识库不存在，无法更新"}, safe=False, status=200)

        # 在更新对应的Pieces
        pieces_slug = stock_pieces.split(",")[1::2]
        pieces_index = stock_pieces.split(",")[0::2]
        for index, slug in zip(pieces_index, pieces_slug):
            try:
                piece = Piece.objects.get(slug=slug)
                piece.index = index
                piece.save()

            except ObjectDoesNotExist:
                 log.warn("Piece {} Is Not In Database Amazing".format(slug))


        return JsonResponse({"errorCode":0, "desc":"更新成功"}, safe=False, status=200)

    def put(self, request, *args, **kwargs):
        update_type = request.data.get("type", "")
        stock_slug = request.data.get("slug", "")
        stock = None

        try:
            stock = Stock.objects.get(slug=stock_slug)
        except ObjectDoesNotExist:
            return JsonResponse({"errorCode":1, "desc":"知识库不存在"}, safe=False, status=200)

        if update_type == "IncreaseSpectate":
            stock.read_count += 1


        elif update_type == "IncreaseMarked":
            stock.marked_count += 1

        stock.save()
        return JsonResponse({"errorCode":0, "desc":"更新成功"}, safe=False, status=200)

class PieceInfo(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        stock_slug = request.GET.get("stock_slug", "")
        piece_slug = request.GET.get("piece_slug", "")

        if piece_slug != "":
            try:
                return JsonResponse({"errorCode": 0, "data":PieceContentForReadSerializer(Piece.objects.get(slug=piece_slug)).data}, safe=False, status=200)
            except ObjectDoesNotExist:
                return JsonResponse({"errorCode": 1}, safe=False, status=200)

        if stock_slug != "":
            return JsonResponse({"errorCode": 0, "data":PieceInfoSerializer(Piece.objects.filter(belong_stock=stock_slug).order_by('index'), many=True).data}, safe=False, status=200)
    
        return JsonResponse({"errorCode": 1}, safe=False, status=200)

    def post(self, request, *args, **kwargs):
        piece_data = request.data["piece_file"]
        piece_name = request.data["piece_file"]._name
        stock_slug = request.data.get("belong_stock_slug", "")
        stock = None

        # 先查一下stock存不存在
        try:
            stock = Stock.objects.get(slug=stock_slug)
        except ObjectDoesNotExist:
            log.warn("SomeOne Want To Attack Our Piece Api Use Stock {}".format(stock_slug))
            return JsonResponse({"errorCode":random.random()}, safe=False, status=200)

        # 查看一下当前的stock有多少页
        pieces_num = len(Piece.objects.filter(belong_stock=stock))
        piece_slug = generate_slug("Piece", stock_slug+piece_name+str(pieces_num))

        # 开始生成
        piece = Piece()
        piece.slug = piece_slug
        piece.name = piece_name
        piece.belong_stock = stock
        piece.content = piece_data
        piece.index = pieces_num + 1
        stock = piece.belong_stock
        stock.upgrade_date = time.strftime("%Y-%m-%d", time.localtime())
        piece.save()
        stock.save()

        return JsonResponse({"errorCode":0, "desc": "新章节上传成功"}, safe=False, status=200)

    def delete(self, request, *args, **kwargs):
        piece_slug = request.GET.get("piece_slug", "")

        try:
            piece = Piece.objects.get(slug=piece_slug)
            piece.delete()

        except ObjectDoesNotExist:
            log.warn("SomeOne Want To Attack Our Piece Api Use Stock {}".format(stock_slug))
            return JsonResponse({"errorCode":random.random()}, safe=False, status=200)

        return JsonResponse({"errorCode":0, "desc": "章节删除成功"}, safe=False, status=200)

    def patch(self, request, *args, **kwargs):
        slug = request.data.get("slug", "")
        name = request.data.get("name", "")
        content = request.data.get("content", "")
        user_slug = request.COOKIES.get("slug", "")
        user = None
        piece = None

        # 先看有没有登陆
        try:
            user = User.objects.get(slug=user_slug)
        except ObjectDoesNotExist:
            return JsonResponse({"errorCode":1, "desc": "不登陆不能随便更新哦"}, safe=False, status=200)

        # 再看章节slug对不对
        try:
            piece = Piece.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return JsonResponse({"errorCode":1, "desc": "章节定位错误，请联系管理员"}, safe=False, status=200)

        # 取出stock的信息，比对用户是否是本人
        if piece.belong_stock.author != user:
            return JsonResponse({"errorCode":1, "desc": "这不是你的知识库哦，不能乱更新"}, safe=False, status=200)

        # 进行更新
        piece.name = name
        stock = piece.belong_stock
        stock.upgrade_date = time.strftime("%Y-%m-%d", time.localtime())
        piece.save()
        stock.save()

        

        if not os.path.exists("Statics/{}".format(piece.content)): 
            return JsonResponse({"errorCode":1, "desc": "章节更新失败，请联系管理员"}, safe=False, status=200)
            
        # 读取文件，识别标题 [ 标题名称， 标题id，标题级别]
        with open("Statics/{}".format(piece.content), "w", encoding="utf-8") as md:
            md.write(content)

        return JsonResponse({"errorCode":0, "desc": "章节更新成功"}, safe=False, status=200)
