# Generated by Django 5.0.1 on 2024-02-06 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0004_alter_companywebsite_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='is_deleted',
            field=models.BooleanField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='companyaddressrole',
            name='is_deleted',
            field=models.BooleanField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='companypersonrole',
            name='is_deleted',
            field=models.BooleanField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='companywebsite',
            name='is_deleted',
            field=models.BooleanField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='is_deleted',
            field=models.BooleanField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='internalmessage',
            name='is_deleted',
            field=models.BooleanField(editable=False, null=True),
        ),
    ]