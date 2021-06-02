from django.contrib import admin
from HelloWorld.Stock.models import Stock

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'author', 'upgrade_date')

admin.site.register(Stock, BookAdmin)