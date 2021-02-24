from django.db import models
from rest_framework.serializers import Serializer
from rest_framework import serializers
from Core.encrypt import generate_slug
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.
class Book(models.Model):
    slug = models.SlugField(blank=False, primary_key=True, default=None, unique=True)
    name = models.CharField(blank=False, db_index=True, max_length=64, default=None)
    author = models.CharField(db_index=True, max_length=64, default=None)
    cover = models.ImageField(upload_to="static/image/cover", default=None)
    content = models.FileField(upload_to="BookData", default=None)

    def save(self):
        self.slug = generate_slug("Book", "{}{}".format(self.name, self.author))
        try:
            already_exist = Book.objects.get(slug=self.slug)
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
    cover = serializers.ImageField()
    
