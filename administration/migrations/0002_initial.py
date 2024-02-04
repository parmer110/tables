# Generated by Django 5.0.1 on 2024-01-24 21:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administration', '0001_initial'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='document',
            field=models.ManyToManyField(blank=True, to='common.document'),
        ),
        migrations.AddField(
            model_name='company',
            name='legal_entity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='common.legalentity'),
        ),
        migrations.AddField(
            model_name='companyaddressrole',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_address_role', to='common.places'),
        ),
        migrations.AddField(
            model_name='companyaddressrole',
            name='job_role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_adress_role', to='common.jobroles'),
        ),
        migrations.AddField(
            model_name='company',
            name='address_roles',
            field=models.ManyToManyField(related_name='companies', to='administration.companyaddressrole'),
        ),
        migrations.AddField(
            model_name='companypersonrole',
            name='job_role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_person_role', to='common.jobroles'),
        ),
        migrations.AddField(
            model_name='companypersonrole',
            name='person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_person_role', to='common.person'),
        ),
        migrations.AddField(
            model_name='company',
            name='personnel_roles',
            field=models.ManyToManyField(related_name='companies', to='administration.companypersonrole'),
        ),
        migrations.AddField(
            model_name='companywebsite',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_website', to='administration.company'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='common.person'),
        ),
        migrations.AddField(
            model_name='internalmessage',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='administration.employee'),
        ),
        migrations.AddField(
            model_name='internalmessage',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='administration.employee'),
        ),
    ]
