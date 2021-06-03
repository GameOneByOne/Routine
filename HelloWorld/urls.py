"""HelloWorld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url
from HelloWorld.Stock.views import StockInfo
from HelloWorld.User.views import UserInfo, EmailCode
from HelloWorld.Reminder.views import ReminderInfo
from . import views


urlpatterns = [
    # HTML View
    path('', views.HomeView),
    path('admin/', admin.site.urls),
    path('viewer/', views.PdfView),
    # path('viewer/', views.PdfView),
        
    # API View 
    re_path('^stock/(?P<slug>[0-9a-zA-Z]{32})$', StockInfo.as_view()),
    path('stock/', StockInfo.as_view()),
    path('user/', UserInfo.as_view()),
    path('user/randomcode', EmailCode.as_view()),
    path('message/', ReminderInfo.as_view()),
    
    
]