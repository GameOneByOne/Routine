from HelloWorld.Users.models import UsersModels
from HelloWorld.Tasks.models import TasksModels
from HelloWorld.Users.serializers import UsersSerializer
from HelloWorld.Tasks.serializers import TasksSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import logging


def InitViews(request):
    return render(request, 'login.html', {"errorLogin": "0"})

@csrf_exempt
def MainViews(request):
    user_id_card = request.GET.get("idCard")
    user_id_password = request.GET.get("idPassword")
    logging.info("We Get A New Custom, He Login's Name Is {}".format(user_id_card))

    try:
        user_info = UsersModels.objects.get(id_care=user_id_card, id_password=user_id_password)
    except ObjectDoesNotExist:
        logging.info("Ooooch Some One Login Failed, Maybe He Input Error id_care Or id_password : {}, {}".format(user_id_card, user_id_password))
        return render(request, 'login.html', {"errorLogin": "1"})

    logging.info("Welcome {}, Have A Good Time".format(user_id_card))
    print(user_info.to_dict())
    return render(request, 'main_page.html', user_info.to_dict())