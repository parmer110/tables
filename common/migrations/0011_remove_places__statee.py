# Generated by Django 4.1.5 on 2023-07-26 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_places__statee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='places',
            name='_statee',
        ),
    ]
