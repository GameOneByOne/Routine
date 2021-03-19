from django.db import models
from HelloWorld.User.models import User
from rest_framework.serializers import Serializer
from rest_framework import serializers
from Core.encrypt import generate_slug
from django.core.exceptions import ObjectDoesNotExist
from HelloWorld.settings import *


def rename_pdf(instance, filename):
    print(instance.slug)
    return "bookData/{}.pdf".format(instance.slug)

# Create your models here.
class Book(models.Model):
    slug = models.SlugField(blank=False, primary_key=True, default=None, unique=True)
    name = models.CharField(blank=False, db_index=True, max_length=256, default=None)
    author = models.CharField(db_index=True, max_length=128, default=None)
    content = models.FileField(upload_to=rename_pdf, default=None)
    upload_date = models.CharField(blank=False, db_index=True, max_length=64, default=None)
    upload_people = models.ForeignKey(to=User, null=True, to_field="slug", related_name="upload_people", on_delete=models.SET_NULL)
        

    def save(self):
        self.slug = generate_slug("Book", "{}{}".format(self.name, self.author))
        try:
            Book.objects.get(slug=self.slug)
        except ObjectDoesNotExist:
            super().save()
            return True
        return False

    class Meta:
        db_table = "Model_Book"

class BookSerializer(serializers.Serializer):
    slug = serializers.SlugField()
    name = serializers.CharField()
    author = serializers.CharField()
    cover = serializers.SerializerMethodField()
    upload_date = serializers.CharField()
    upload_people = serializers.CharField(source='upload_people.user_name')
        

    def get_cover(self, obj):
        return PDF_COVER_PATH + obj.slug + ".jpeg"
    
