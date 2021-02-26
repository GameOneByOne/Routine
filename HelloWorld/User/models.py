from django.db import models
from Core.encrypt import generate_slug
import datetime

# Create your models here.
class User(models.Model):
    slug = models.SlugField(blank=False, primary_key=True, default=None, unique=True)
    account = models.CharField(blank=False, db_index=True, max_length=64, default=None)
    user_name = models.CharField(blank=False, db_index=True, max_length=64, default="未填写")
    password = models.CharField(blank=False, max_length=64, default=None)
    birthday = models.DateField(null=True, default="1990-01-01")
    email = models.EmailField(null=True, default=None)
    phone = models.CharField(null=True, max_length=16, default=None)
    avatar_url = models.ImageField(upload_to="static/image/static/", default=None)

    def save(self):
        self.slug = generate_slug("User", "{}{}".format(self.account, self.password))
        super().save()

    class Meta:
        db_table = "Model_User"

