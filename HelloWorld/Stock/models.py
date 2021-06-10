from django.db import models
from HelloWorld.User.models import User
from rest_framework import serializers
from HelloWorld.settings import *
import re
import os


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
    tag = serializers.CharField()

    def get_author_name(self, obj):
        return obj.author.user_name

    def get_author_avatar(self, obj):
        return obj.author.avatar_id

    def get_author_slug(self, obj):
        return obj.author.slug

    def get_cover(self, obj):
        return "" if obj.cover.name == "undefined" else "/static/" + obj.cover.name



class PieceSerializer(serializers.Serializer):
    slug = serializers.SlugField()
    name = serializers.CharField()
    belong_stock = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    def get_belong_stock(self, obj):
        return obj.belong_stock.slug

    def get_content(self, obj):
        return "/static/" + obj.content.name

class PieceContentSerializer(serializers.Serializer):
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        # 记录五个级别的标题顺序
        tilte_one = 0
        tilte_two = 0
        tilte_three = 0
        tilte_four = 0
        tilte_five = 0
        result = list()
        min_title_level = 5
        content = ""
        index = 0

        if not os.path.exists("Statics/{}".format(obj.content)): return result
            
        # 读取文件，识别标题 [ 标题名称， 标题id，标题级别]
        with open("Statics/{}".format(obj.content), "r", encoding="utf-8") as md:
            temp_result = list()
            for line in md.readlines():
                line = line.strip(" ")
                
                is_title = re.match("#{1,5}", line)
                if is_title:
                    index += 1
                    # 这里判断是几级标题
                    temp_line = line
                    title_level = len(is_title.group())
                    title_name = temp_line.replace(is_title.group(), "")

                    min_title_level = title_level if min_title_level > title_level else min_title_level
                    result.append([title_name.strip(), "{}-title-{}".format(obj.slug, index), title_level])

                    # 生成新的标题
                    new_title = len(is_title.group()) * "#" + " " + "<p id='{}-title-{}'>".format(obj.slug, index) + title_name + "</p>"
                    content += new_title

                else:
                    content += line


        return {"slug":obj.slug, "rows": result, "content": content, "min_title_level": min_title_level}