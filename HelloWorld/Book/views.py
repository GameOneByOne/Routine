from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from HelloWorld.Book.models import Book, BookSerializer
from HelloWorld.User.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from Core import improcess
import time
from HelloWorld.settings import * 
from HelloWorld.settings import logger as log
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

        return JsonResponse(BookSerializer(Book.objects.all(), many=True).data[page_num:page_num+12], safe=False, status=200)

    def post(self, request, *args, **kwargs):
        book = Book()
        book.name = request.data["bookName"] if request.data.get("bookName", "") != "" else request.data["pdf_file"]._name.split(".")[0]
        book.author = request.data["bookAuthor"] if request.data.get("bookAuthor", "") != "" else "未命名作者"
        book.upload_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        if request.COOKIES.get("slug", "null") == "null" or request.COOKIES.get("slug", "null") == "undefined": 
            book.upload_people = User.objects.get(slug="Default")
        else: 
            book.upload_people = User.objects.get(slug=request.COOKIES.get("slug", "Default"))
        book.content = request.data["pdf_file"]

        if book.save():
            log.info("Book Data Parse Success , Begin To Generate And Resize Cover And Split Pdf")
            if improcess.generate_pdf_cover(book.slug+".pdf", book.slug+".jpeg") and \
                improcess.update_image_size(book.slug+".jpeg", book.slug+".jpeg") and \
                improcess.split_pdf("Statics/bookData/{}.pdf".format(book.slug)): 

                return JsonResponse({"errorCode":0, "content":""}, safe=False, status=200)
            else:
                Book.objects.get(slug=book.slug).delete()
                return JsonResponse({"errorCode":1, "content":""}, safe=False, status=200)

        return JsonResponse({"errorCode":1, "content":""}, safe=False, status=200)


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
