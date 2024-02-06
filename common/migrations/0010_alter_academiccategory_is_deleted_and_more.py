# Generated by Django 5.0.1 on 2024-02-06 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_academiccategory_is_deleted_academicrank_is_deleted_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academiccategory',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='academicrank',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='academicrecord',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='appmodels',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='classification',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='dateslot',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='dynamictabletest1',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='dynamictabletest2',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='educationaldegree',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='fieldofstudy',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='legalentity',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='legalentityplaces',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='legaltypes',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='loginrecord',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='path',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='personplace',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='pictures',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='places',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='scheduleplan',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='setting',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='settingmenus',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='sitemanagementlog',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='systemsettingspic',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='tokenlifetime',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='translate',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='university',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='universityplaces',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='usersession',
            name='is_deleted',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
    ]