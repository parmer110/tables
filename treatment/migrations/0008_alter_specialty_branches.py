# Generated by Django 4.1.5 on 2023-07-27 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treatment', '0007_specialty_branches'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialty',
            name='branches',
            field=models.CharField(choices=[('specialties', 'specialties'), ('__pycache__', '__pycache__')], max_length=100, null=True),
        ),
    ]
