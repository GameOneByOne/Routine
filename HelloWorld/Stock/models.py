from django.db import models
from HelloWorld.User.models import User
from rest_framework import serializers
from HelloWorld.settings import *


def save_cover(instance, filename):
    return "Stock/{}/cover/{}.{}".format(instance.slug, instance.slug, filename.split(".")[-1])

def save_piece(instance, filename):
    return "Stock/{}/piece/{}.md".format(instance.slug, instance.slug)

class Stock(models.Model):
    slug = models.SlugField(blank=False, primary_key=True, default=None, unique=True)
    name = models.CharField(blank=False, db_index=True, max_length=256, default=None)
    author = models.ForeignKey(to=User, null=True, to_field="slug", related_name="author", on_delete=models.SET_NULL)
    cover = models.FileField(upload_to=save_cover, default=None)
    upgrade_date = models.CharField(blank=False, db_index=True, max_length=64, default=None)
    public = models.BooleanField(default=False)
    marked_count = models.IntegerField(blank=False, db_index=True, default=0)
    read_count = models.IntegerField(blank=False, db_index=True, default=0)
    describe = models.CharField(max_length=128, default="")
    tag = models.CharField(max_length=64, default="")

    def save(self):
        super().save()

    class Meta:
        db_table = "Model_Stock"


class Piece(models.Model):
    slug = models.SlugField(blank=False, primary_key=True, default=None, unique=True)
    name = models.CharField(blank=False, max_length=256, default=None)
    belong_stock = models.ForeignKey(to=Stock, db_index=True, null=True, to_field="slug", related_name="belong_stock", on_delete=models.SET_NULL)
    index = models.IntegerField(blank=False, default=0)
    content = models.FileField(upload_to=save_piece, default=None)


    def save(self):
        super().save()
        
    class Meta:
        db_table = "Model_Piece"

class StockSerializer(serializers.Serializer):
    slug = serializers.SlugField()
    name = serializers.CharField()
    author_slug = serializers.SerializerMethodField()
    author_avatar = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    upgrade_date = serializers.CharField()
    public = serializers.BooleanField()
    marked_count = serializers.IntegerField()
    read_count = serializers.IntegerField()
    describe = serializers.CharField()
    tag = serializers.SerializerMethodField()

    def get_author_name(self, obj):
        return obj.author.user_name

    def get_author_avatar(self, obj):
        return obj.author.avatar_id

    def get_author_slug(self, obj):
        return obj.author.slug

    def get_cover(self, obj):
        return "" if obj.cover.name == "undefined" else "/static/" + obj.cover.name

    def get_tag(self, obj):
        return obj.tag.split(",")


class PieceSerializer(serializers.Serializer):
    slug = serializers.SlugField()
    name = serializers.CharField()
    belong_stock = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    index = serializers.IntegerField()

    def get_belong_stock(self, obj):
        return obj.belong_stock.slug

    def get_content(self, obj):
        return "/static/" + obj.content.name