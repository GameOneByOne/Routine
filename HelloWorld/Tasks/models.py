from django.db import models

# Create your models here.
class TasksModels(models.Model):
    name = models.CharField(max_length=128) # 任务名称
    slug = models.SlugField(default=None) # 任务标识
    label = models.CharField(max_length=32, default=None) # 任务标签
    begin_date = models.DateField(default=None) # 任务开始时间
    deadline = models.DateField(default=None) # 任务计划完成时间
    finish_date = models.DateField(default=None) # 任务实际完成时间
    task_history = models.TextField(default=None) # 任务变更历史
    finished = models.BooleanField(default=False) # 是否完成
    belong_to = models.ForeignKey("Users.UsersModels", related_name="tasks",null=False, blank=True, on_delete=models.CASCADE)

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

