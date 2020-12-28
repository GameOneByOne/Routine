from rest_framework import serializers
from .models import TasksModels


class TasksSerializer(serializers.ModelSerializer):

    class Meta:
        model = TasksModels
        fields = ('name', 'begin_date', 'deadline')
