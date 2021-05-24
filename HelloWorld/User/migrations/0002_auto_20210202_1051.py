# Generated by Django 3.1 on 2021-02-02 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default=None, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(default=None, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=models.SlugField(default=None, primary_key=True, serialize=False, unique=True),
        ),
    ]
