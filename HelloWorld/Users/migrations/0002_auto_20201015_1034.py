# Generated by Django 3.0.8 on 2020-10-15 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersmodels',
            name='name',
        ),
        migrations.AddField(
            model_name='usersmodels',
            name='id_care',
            field=models.CharField(default=None, max_length=128),
        ),
        migrations.AddField(
            model_name='usersmodels',
            name='id_password',
            field=models.CharField(default=None, max_length=128),
        ),
    ]
