from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UsersModels
from .serializers import UsersSerializer
from HelloWorld.Tasks.serializers import TasksSerializer
from HelloWorld.Tasks.models import TasksModels
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class Users(APIView):

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
 
    def get(self, request, *args, **kwargs):
        query_name = request.GET.get("name")
        try:
            user_info = UsersModels.objects.get(name=query_name)
        except ObjectDoesNotExist:
            return Response("No User")

        for task in user_info.tasksmodels_set.all():
            print(TasksSerializer(task).data)
        return Response(UsersSerializer(user_info).data)
 
    def post(self, request, *args, **kwargs):
        new_user = UsersSerializer(data=request.data)
        print(request.data)
        if new_user.is_valid(raise_exception=True):
            new_user.save()
            return Response('Login In Success')

        return Response('Login In Failed')
        