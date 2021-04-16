from django.db import models
from rest_framework.serializers import Serializer
from rest_framework import serializers
from Core.encrypt import generate_slug, md5
import datetime

# Create your models here.
class User(models.Model):
    slug = models.SlugField(blank=False, primary_key=True, default=None, unique=True)
    email = models.EmailField(null=True, default=None)
    user_name = models.CharField(blank=False, db_index=True, max_length=64, default="Sharer")
    password = models.CharField(blank=False, max_length=64, default=None)
    avatar_id = models.CharField(blank=True, max_length=64, default="")

    def save(self):
        self.slug = generate_slug("User", "{}{}".format(self.email, self.password))
        self.password = md5(self.password)

        if self.avatar_id == "": self.avatar_id = md5(self.email)[:18]
        super().save()

    class Meta:
        db_table = "Model_User"


class UserSerializer(serializers.Serializer):
    slug = serializers.SlugField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    user_name = serializers.CharField(required=False)
    avatar_id = serializers.CharField(required=False)

    def create(self, validated_data, *args, **kargs):
        user = User(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.slug = validated_data.get('slug',instance.slug)
        instance.email = validated_data.get('email',instance.email)
        instance.password = validated_data.get('password',instance.password)
        instance.user_name = validated_data.get('user_name',instance.user_name)
        instance.avatar_id = validated_data.get('avatar_id',instance.avatar_id)
        instance.save()
        return instance