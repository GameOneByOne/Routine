from django.contrib import admin
from HelloWorld.User.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('slug', 'email', 'user_name', 'super_user')

admin.site.register(User, UserAdmin)
