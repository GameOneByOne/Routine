# Generated by Django 3.1 on 2021-02-22 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0003_auto_20210201_1720'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='data',
            new_name='content',
        ),
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(default=None, upload_to='static/image/cover'),
        ),
        migrations.AlterField(
            model_name='book',
            name='slug',
            field=models.SlugField(default=None, primary_key=True, serialize=False, unique=True),
        ),
    ]
