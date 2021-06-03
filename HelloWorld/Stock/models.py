from django.db import models
from HelloWorld.User.models import User
from rest_framework import serializers
from HelloWorld.settings import *


# def save_md(instance, filename):
#     return "Stock/{}/{}.md".format(instance.slug, instance.slug)

def save_cover(instance, filename):
    return "Stock/{}/cover/{}.{}".format(instance.slug, instance.slug,filename.split(".")[-1])

def save_piece(instance, filename):
    return "Stock/{}/piece/{}.md".format(instance.slug, ".".join(filename.split(".")[:-1]))

class Stock(models.Model):
    slug = models.SlugField(blank=False, primary_key=True, default=None, unique=True)
    name = models.CharField(blank=False, db_index=True, max_length=256, default=None)
    author = models.ForeignKey(to=User, null=True, to_field="slug", related_name="author", on_delete=models.SET_NULL)
    cover = models.FileField(upload_to=save_cover, default=None)
    upgrade_date = models.CharField(blank=False, db_index=True, max_length=64, default=None)
    public = models.BooleanField(default=False)
    marked_count = models.IntegerField(blank=False, db_index=True, default=0)
    read_count = models.IntegerField(blank=False, db_index=True, default=0)
    tag = models.CharField(max_length=64, default="")

    def save(self):
        super().save()

    class Meta:
        db_table = "Model_Stock"

class StockSerializer(serializers.Serializer):
    slug = serializers.SlugField()
    name = serializers.CharField()
    author = serializers.CharField()
    cover = serializers.FileField()
    upgrade_date = serializers.CharField()
    public = serializers.BooleanField()
    marked_count = serializers.IntegerField()
    read_count = serializers.IntegerField()
    tag = serializers.SerializerMethodField()

    def get_tag(self, obj):
        return obj.tag.split(",")
    
