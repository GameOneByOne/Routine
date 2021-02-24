from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from HelloWorld.Book.models import Book, BookSerializer
from django.http import JsonResponse


# Create your views here.
class BookInfo(APIView):
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        return JsonResponse(BookSerializer(books, many=True).data, safe=False, status=200)

    def post(self, request, *args, **kwargs):
        print("Book Update")
        data = {
            'data': 'post success'
        }
        return JsonResponse(data, safe=False, status=200)

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