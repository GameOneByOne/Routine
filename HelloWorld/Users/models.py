from django.db import models
from ..CommonVar import COLLEGES

# Create your models here.
class UsersModels(models.Model):
    id_care = models.CharField(max_length=128, default=None) # 用户登录的账号
    id_password = models.CharField(max_length=128, default=None) # 用户登录的密码
    slug = models.SlugField(max_length=64, default=None) # 用户唯一标识
    username = models.CharField(max_length=128, default=None) # 用户显示的昵称
    email = models.EmailField(default=None) # 用户的邮箱
    birthday = models.DateField(default=None) # 用户的生日
    phone = models.CharField(max_length=15, primary_key=True, default=None) # 用户的手机号
    undergraduate_college = models.CharField(max_length=10, choices=COLLEGES, default="none") # 用户的本科学校
    dream_college = models.CharField(max_length=128) # 用户的梦想学校
    user_mask = models.BinaryField(default=0) # 用户状态掩码，用来标记一些事件
    team = models.ForeignKey("Teams.TeamsModels",related_name="team",null=True, blank=True, default=None, on_delete=models.SET_NULL) # 用户所加入的小组

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
 

