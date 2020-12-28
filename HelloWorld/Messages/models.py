from django.db import models
from HelloWorld.Users.models import UsersModels

# Create your models here.
class MessagesModels(models.Model):
    context = models.TextField() # 私信内容
    slug = models.SlugField() # 私信标识
    sender = models.SlugField() # 发送人
    send_date = models.DateField() # 发送日期
    read = models.BooleanField() # 是否已读
    message_to = models.OneToOneField(UsersModels, on_delete=models.CASCADE) # 要发给的人

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

