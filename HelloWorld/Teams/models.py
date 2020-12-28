from django.db import models

# Create your models here.
class TeamsModels(models.Model):
    name = models.CharField(max_length=64) # 小组名称
    slug = models.SlugField() # 小组标识
    slogan = models.CharField(max_length=256) # 小组口号

    def to_dict(self, fields=None, exclude=None):
        data = {}

        for f in self._meta.concrete_fields + self._meta.many_to_many:
            value = f.value_from_object(self)

            if fields and f.name not in fields:
                continue

            if exclude and f.name in exclude:
                continue

            if isinstance(f, models.ManyToManyField):
                value = [ i.id for i in value ] if self.pk else None

            if isinstance(f, models.DateTimeField):
                value = value.strftime('%Y-%m-%d %H:%M:%S') if value else None

            data[f.name] = value

        return data

