from django.db import models

# Create your models here.
# class CommentsModels(models.Model):
#     critic = models.CharField(max_length=128) # 评论人
#     slug = models.SlugField() # 评论标识
#     context = models.TextField() # 评论内容
#     belong_to_tasks = models.ForeignKey("Tasks.TasksModels") # 评论归属的任务
#     belong_to_comments = models.ForeignKey("Comments.CommentsModels") # 评论归属的子评论

#     def to_dict(self, fields=None, exclude=None):
#         data = {}

#         for f in self._meta.concrete_fields + self._meta.many_to_many:
#             value = f.value_from_object(self)

#             if fields and f.name not in fields:
#                 continue

#             if exclude and f.name in exclude:
#                 continue

#             if isinstance(f, models.ManyToManyField):
#                 value = [ i.id for i in value ] if self.pk else None

#             if isinstance(f, models.DateTimeField):
#                 value = value.strftime('%Y-%m-%d %H:%M:%S') if value else None

#             data[f.name] = value

#         return data

