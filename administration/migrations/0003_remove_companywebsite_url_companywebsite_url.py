# Generated by Django 5.0.1 on 2024-01-30 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0002_initial'),
        ('common', '0004_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companywebsite',
            name='url',
        ),
        migrations.AddField(
            model_name='companywebsite',
            name='url',
            field=models.ManyToManyField(related_name='company_website', to='common.path'),
        ),
    ]
