from django.db import models

# Create your models here.
class Book(models.Model):
    slug = models.SlugField(blank=False, primary_key=True, default=None, unique=True)
    name = models.CharField(blank=False, db_index=True, max_length=64, default=None)
    author = models.CharField(db_index=True, max_length=64, default=None)
    cover = models.ImageField(default=None)
    data = models.FileField(upload_to="BookData", default=None)

    class Meta:
        db_table = "Model_Book"
    
