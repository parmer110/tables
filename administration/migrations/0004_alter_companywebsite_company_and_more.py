# Generated by Django 5.0.1 on 2024-01-30 09:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0003_remove_companywebsite_url_companywebsite_url'),
        ('common', '0004_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companywebsite',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_websites', to='administration.company'),
        ),
        migrations.AlterField(
            model_name='companywebsite',
            name='url',
            field=models.ManyToManyField(related_name='company_websites', to='common.path'),
        ),
    ]
