# Generated by Django 3.1.5 on 2021-02-28 01:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0007_auto_20210226_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='cover',
        ),
    ]