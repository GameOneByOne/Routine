from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TasksModels
from .serializers import TasksSerializer
from HelloWorld.Users.models import UsersModels

# Create your views here.
class Tasks(APIView):
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get("phone", "")
 
    def post(self, request, *args, **kwargs):
        new_user = TasksModels(name=request.data.get("name", ""),
                                begin_date=request.data.get("begin_date", ""),
                                deadline=request.data.get("deadline", "")
                                )
        new_user.belong_to = UsersModels.objects.last()
        print(new_user)

        new_user.save()

        return Response('Add Task Success')
        

"""

{
	"name":"Math",
	"begin_date":"2000-01-01",
	"deadline":"2000-01-02",
	"phone":"18711563442"
}
"""