from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import logging


def LoginView(request):    
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'login.html', context)

def HomeView(request):    
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'home.html', context)