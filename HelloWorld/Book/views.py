from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from HelloWorld.Book.models import Book, BookSerializer
from HelloWorld.User.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from Core.encrypt import generate_slug
import time
from HelloWorld.settings import * 
from HelloWorld.settings import logger as log
from HelloWorld.ProcessQueue.apps import pQueueManager
import os


# Create your views here.
class BookInfo(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.GET.get("slug", "") != "":
            book_path = "Statics/bookData/{}".format(request.GET["slug"])
            try:
                book_info = BookSerializer(Book.objects.get(slug=request.GET["slug"])).data
                book_info["pieces"] = os.listdir(book_path)
                if IS_UNIX: book_info["pieces"].reverse()
                return JsonResponse(book_info, safe=False, status=200)

            except ObjectDoesNotExist:
                return JsonResponse({}, safe=False, status=200)

        page_num = int(request.COOKIES["page_num"])

        return JsonResponse(BookSerializer(Book.objects.filter(public=True), many=True).data[page_num:page_num+12], safe=False, status=200)

    def post(self, request, *args, **kwargs):
        book_name = request.data["bookName"] if request.data.get("bookName", "") != "" else request.data["pdf_file"]._name.split(".")[0]
        book_author = request.data["bookAuthor"] if request.data.get("bookAuthor", "") != "" else "未命名作者"
        book_slug = generate_slug("Book", "{}".format(book_name))
        
        try:
            Book.objects.get(slug=book_slug)
            return JsonResponse({"errorCode":1, "desc":"书名重复"}, safe=False, status=200)

        except ObjectDoesNotExist:
            book = Book()
            book.name = book_name
            book.author = book_author
            book.slug = book_slug
            book.upload_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            book.public = False

            if (request.COOKIES.get("slug", "null") != "null") and (request.COOKIES.get("slug", "null") == "undefined"): 
                book.upload_people = User.objects.get(slug=request.COOKIES.get("slug", "Default"))
                
            book.content = request.data["pdf_file"]
            book.save()

            log.info("Book Data Parse Success , Begin To Generate And Resize Cover And Split Pdf")
            pQueueManager.push("ProcessBookQueue", [request.COOKIES.get("csrftoken", ""), book.slug])

            return JsonResponse({"errorCode":0, "desc":"上传成功啦，等后台处理完成，就可以浏览啦"}, safe=False, status=200)
