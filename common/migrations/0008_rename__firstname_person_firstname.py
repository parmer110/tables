# Generated by Django 4.1.5 on 2023-07-23 02:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_alter_person__firstname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='_firstname',
            new_name='firstname',
        ),
    ]
