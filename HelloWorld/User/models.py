from django.db import models

# Create your models here.
class User(models.Model):
    slug = models.SlugField(blank=False, primary_key=True, default=None, unique=True)
    account = models.CharField(blank=False, db_index=True, max_length=64, default=None)
    password = models.CharField(blank=False, max_length=64, default=None)
    birthday = models.DateField(default=None)
    email = models.EmailField(default=None)
    phone = models.CharField(max_length=16, default=None)


    def save(self, account="", password="", birthday="", email="", phone=""):

        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )
        self.the_id = self._create_the_id()


    class Meta:
        db_table = "Model_User"

