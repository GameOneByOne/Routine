from django.db import models
from rest_framework.serializers import Serializer
from rest_framework import serializers
from Core.encrypt import generate_slug
from django.core.exceptions import ObjectDoesNotExist


def rename_cover(instance, filename):
    return "image/pdf_cover/{}.jpeg".format(instanch.slug)

def rename_pdf(instance, filename):
    return "bookData/{}.pdf".format(instance.slug)

# Create your models here.
class Book(models.Model):
    slug = models.SlugField(blank=False, primary_key=True, default=None, unique=True)
    name = models.CharField(blank=False, db_index=True, max_length=64, default=None)
    author = models.CharField(db_index=True, max_length=64, default=None)
    cover = models.ImageField(upload_to=rename_cover, default=None)
    content = models.FileField(upload_to=rename_pdf, default=None)

    def generate_book_slug(self):
        self.slug = generate_slug("Book", "{}{}".format(self.name, self.author))
        return self.slug

    def save(self):
        
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
    
