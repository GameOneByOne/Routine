# Generated by Django 3.0.8 on 2020-10-19 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Teams', '0001_initial'),
        ('Users', '0006_usersmodels_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersmodels',
            name='team',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team', to='Teams.TeamsModels'),
        ),
    ]
