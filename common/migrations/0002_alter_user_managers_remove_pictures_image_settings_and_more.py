# Generated by Django 5.0.1 on 2024-01-28 22:49

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='pictures',
            name='image_settings',
        ),
        migrations.AddField(
            model_name='pictures',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='picture', to=settings.AUTH_USER_MODEL),
        ),
    ]
