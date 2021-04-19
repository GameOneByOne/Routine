from django.contrib import admin
from HelloWorld.Book.models import Book

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'author', 'upload_date', 'upload_people', 'public')

admin.site.register(Book, BookAdmin)