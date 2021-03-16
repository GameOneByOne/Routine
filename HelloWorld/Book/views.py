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
import logging
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
                return JsonResponse(book_info, safe=False, status=200)

            except ObjectDoesNotExist:
                return JsonResponse({}, safe=False, status=200)

        return JsonResponse(BookSerializer(Book.objects.all(), many=True).data, safe=False, status=200)

    def post(self, request, *args, **kwargs):
        if len(request.data) == 0: 
            logging.info("Request POST BOOK Api , But Have No Data Upload, So Return 1")
            return JsonResponse({"errorCode":1}, safe=False, status=200)

        book = Book()
        book.name = request.data["bookName"] if request.data.get("bookName", "") != "" else "未命名PDF"
        book.author = request.data["bookAuthor"] if request.data.get("bookAuthor", "") != "" else "未命名作者"
        book.upload_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        book.upload_people = User.objects.get(slug=request.COOKIES.get("slug", ""))
        book.content = request.data["pdf_file"]

        if book.save():
            logging.info("Book Data Parse Success , Begin To Generate And Resize Cover And Split Pdf")
            if not improcess.generate_pdf_cover(book.slug+".pdf", book.slug+".jpeg"): 
                return JsonResponse({"errorCode":1, "content":""}, safe=False, status=200)

            if not improcess.update_image_size(book.slug+".jpeg", book.slug+".jpeg"):
                return JsonResponse({"errorCode":1, "content":""}, safe=False, status=200)

            if not improcess.split_pdf("Statics/bookData/{}.pdf".format(book.slug)):
                return JsonResponse({"errorCode":1, "content":""}, safe=False, status=200)

            return JsonResponse({"errorCode":0, "content":""}, safe=False, status=200)

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
