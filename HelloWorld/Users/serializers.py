from rest_framework import serializers
from .models import UsersModels
from ..CommonVar import COLLEGES


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsersModels
        fields = ('username', 'birthday', 'phone', 'undergraduate_college', 'dream_college')
