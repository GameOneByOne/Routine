from django.db import models

# Create your models here.
class Book(models.Model):
    name = models.CharField(null=False, blank=False, db_index=True, max_length=64)
    author = models.CharField(db_index=True, max_length=64)
    upload_date = models.DateField(null=False, auto_now_add=True, db_index=True)
    upload_person = models.CharField(null=False, db_index=True, max_length=16)
    series_no = models.CharField(null=False, primary_key=True, db_index=True, max_length=64)

    class Meta:
        db_table = "Model_Book"
    
