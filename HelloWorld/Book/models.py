from django.db import models
from HelloWorld.User.models import User
from rest_framework.serializers import Serializer
from rest_framework import serializers
from Core.encrypt import generate_slug
from django.core.exceptions import ObjectDoesNotExist
from HelloWorld.settings import *


def rename_pdf(instance, filename):
    return "bookData/{}.pdf".format(instance.slug)

class Book(models.Model):
    slug = models.SlugField(blank=False, primary_key=True, default=None, unique=True)
    name = models.CharField(blank=False, db_index=True, max_length=256, default=None)
    author = models.CharField(db_index=True, max_length=128, default=None)
    content = models.FileField(upload_to=rename_pdf, default=None)
    upload_date = models.CharField(blank=False, db_index=True, max_length=64, default=None)
    upload_people = models.ForeignKey(to=User, null=True, to_field="slug", related_name="upload_people", on_delete=models.SET_NULL)
    public = models.BooleanField(default=False)
    tag =  models.CharField(max_length=64, default="")

    def save(self):
        super().save()

    class Meta:
        db_table = "Model_Book"

class BookSerializer(serializers.Serializer):
    slug = serializers.SlugField()
    name = serializers.CharField()
    author = serializers.CharField()
    cover = serializers.SerializerMethodField()
    upload_date = serializers.CharField()
    upload_people = serializers.SerializerMethodField()
    tag = serializers.CharField()
        
    def get_upload_people(self, obj):
        if obj.upload_people: return obj.upload_people.user_name
        return "未命名" 

    def get_cover(self, obj):
        return PDF_COVER_PATH + obj.slug + ".jpeg"

    def get_tag(self, obj):
        return obj.tag.split(",")
    
