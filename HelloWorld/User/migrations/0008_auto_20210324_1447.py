# Generated by Django 3.1 on 2021-03-24 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0007_auto_20210317_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avatar_url',
        ),
        migrations.AddField(
            model_name='user',
            name='avatar_id',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
    ]
