from django.db import models
from HelloWorld.Users.models import UsersModels

# Create your models here.
class NotificationsModels(models.Model):
    context = models.TextField(default=None) # 通知内容
    read = models.BooleanField(default=False) # 是否已读
    notify_to = models.OneToOneField(UsersModels, on_delete=models.CASCADE) # 消息通知人

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

