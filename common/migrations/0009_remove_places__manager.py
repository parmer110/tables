# Generated by Django 4.1.5 on 2023-07-26 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_remove_places__statee_places__address_places__city_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='places',
            name='_manager',
        ),
    ]
