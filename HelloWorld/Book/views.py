from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from HelloWorld.Book.models import Book, BookSerializer
from django.http import JsonResponse
from Core import improcess


# Create your views here.
class BookInfo(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        return JsonResponse(BookSerializer(books, many=True).data, safe=False, status=200)

    def post(self, request, *args, **kwargs):
        print(request.data)
        book = Book()
        data = request.data["fileId"].split(".")[0].split("_")

        if len(data) < 2: return JsonResponse({"errorCode":1}, safe=False, status=200)
        elif len(data) == 3: book.name, book.author = data[1], data[2]
        else: book.name, book.author = data[1], ""

        book.content = request.data["pdf_file"]
        slug = book.generate_book_slug()
        book.save()

        improcess.generate_pdf_cover(book.slug+".pdf", book.slug+".jpeg")
        improcess.update_image_size(book.slug+".jpeg", book.slug+".jpeg")

        Book.objects.filter(slug=slug).update(cover="static/image/pdf_cover/{}".format(book.slug+".jpeg"))

        if book.save(): return JsonResponse({"errorCode":0}, safe=False, status=200)
        return JsonResponse({"errorCode":1}, safe=False, status=200)


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