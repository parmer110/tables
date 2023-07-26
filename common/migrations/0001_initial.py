# Generated by Django 4.1.5 on 2023-07-26 10:14

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('createddtm', models.DateTimeField(auto_now_add=True)),
                ('updatedtm', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('_firstname', models.TextField(db_column='firstname', null=True, verbose_name='First Name')),
                ('_lastname', models.TextField(db_column='lastname', null=True, verbose_name='Last Name')),
                ('_birthdate', models.TextField(db_column='birthdate', null=True, verbose_name='Birthdate')),
                ('_national_code', models.TextField(db_column='national_code', null=True, verbose_name='National Code')),
                ('_passport_number', models.TextField(db_column='passport_number', null=True, verbose_name='Passport Number')),
                ('_sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], db_column='sex', max_length=496, null=True, verbose_name='Sex')),
                ('_mobile_phone', models.TextField(db_column='mobile_phone', null=True, verbose_name='Mobile Phone')),
                ('_address', models.TextField(db_column='address', null=True, verbose_name='Address')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SiteManagementsLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('createddtm', models.DateTimeField(auto_now_add=True)),
                ('updatedtm', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('_ip4', models.CharField(db_column='ip4', max_length=558, null=True, verbose_name='IP4')),
                ('_ip6', models.CharField(db_column='ip6', max_length=990, null=True, verbose_name='IP6')),
                ('_link', models.TextField(db_column='link', null=True, verbose_name='Link')),
                ('_action', models.TextField(db_column='action', null=True, verbose_name='Action')),
                ('_person', models.ForeignKey(db_column='person', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='SiteManagementsLog', to='common.person', verbose_name='Person')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Places',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('createddtm', models.DateTimeField(auto_now_add=True)),
                ('updatedtm', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('_title', models.CharField(db_column='title', max_length=1166, null=True, verbose_name='Title')),
                ('_country', models.CharField(db_column='country', max_length=686, null=True, verbose_name='Country')),
                ('_statee', models.CharField(db_column='state', max_length=686, null=True, verbose_name='State')),
                ('_city', models.CharField(db_column='city', max_length=686, null=True, verbose_name='City')),
                ('_address', models.CharField(db_column='address', max_length=1966, null=True, verbose_name='Address')),
                ('_postalcode', models.CharField(db_column='postalcode', max_length=606, null=True, verbose_name='Postalcode')),
                ('_phoneNumber', models.CharField(db_column='phone_number', max_length=606, null=True, verbose_name='Phone Number')),
                ('_usage', models.TextField(db_column='usage', null=True, verbose_name='Usage')),
                ('_manager', models.ForeignKey(db_column='manager', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Places', to='common.person', verbose_name='Manager')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
