from safedelete.models import SafeDeleteModel
from django.contrib.auth.models import AbstractUser, Group as UserRole, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.apps import apps
from django.db import models
import datetime
from django.utils import timezone
from datetime import timedelta
import re
from django.core.validators import MaxValueValidator
from PIL import Image
from django.db.models.signals import post_delete, post_save, pre_save, pre_delete, post_migrate
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
import os
from django.contrib import messages
from django.contrib.sessions.models import Session
from phonenumber_field.modelfields import PhoneNumberField
import pdb
from django.core.cache import cache
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken as JWTBlacklistedToken
from django.contrib.sessions.models import Session
import uuid
import shutil
from common.utils.crypto import encoder, decoder
from common.utils.tools import *


# Index:
    # CommonModel (Abstract)
    # User
    # Person
    # Place
    # PersonPlace
    # SiteManagementsLog
    #Translate

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class AllManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()        

class CommonModel(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)
    deleted_at = models.DateTimeField(editable=False, null=True)

    objects = ActiveManager()
    all_objects = AllManager()

    def delete(self, *args, **kwargs):

        unique_fields = [
            field for field in self._meta.get_fields()
            if (
                not field.auto_created and
                not isinstance(field, (models.AutoField, models.BigAutoField)) and
                (isinstance(field, models.OneToOneField) or 
                field.unique
                )
            )
        ]

        for field in unique_fields:
            value = getattr(self, field.name)
            if value is not None and value != '':
                if isinstance(field, models.OneToOneField):
                    setattr(self, field.name, None)
                elif isinstance(field, (models.DateField, models.DateTimeField)):
                    delta = timedelta(days=1)
                    unique_value = value + delta
                    setattr(self, field.name, unique_value)
                else:
                    max_length = field.max_length if hasattr(field, 'max_length') else None
                    unique_value = (
                        f"{value}-{uuid.uuid4()}" if isinstance(value, str) 
                        else value + 1 if isinstance(value, int)
                        else f"{value}-{uuid.uuid4()}"
                    )
                    if max_length and len(str(unique_value)) > max_length:
                        unique_value = str(unique_value)[:max_length]

                    setattr(self, field.name, unique_value)

        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        abstract = True

class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    ipv4_address = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    ipv6_address = models.GenericIPAddressField(protocol='IPv6', null=True, blank=True)
    action = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, request=None, *args, **kwargs):
        if request:
            self.ipv4_address = request.META.get('REMOTE_ADDR')
            self.ipv6_address = request.META.get('HTTP_X_FORWARDED_FOR')
        super().save(*args, **kwargs)

@receiver(post_save)
def create_audit_log_on_save(sender, instance, created, **kwargs):
    excluded_models = (
    AuditLog, 
    MyCounter, 
    Session, 
    UserSession, 
    LoginRecord, 
    BlacklistedToken, 
    JWTBlacklistedToken,
    OutstandingToken, 
    Session, 
)
    if sender in excluded_models:
        return

    print("♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠")
    print(sender)
    # Clear chaches
    cache.client.delete_pattern('settings_serialized_model_*')
    if sender == SettingMenus:
        cache.client.delete_pattern('setting_table_index_view_set_retrieve_*')
    if sender == AppModels:
        cache.client.delete_pattern('*table_title*')

    if created:
        action = "Created"
    else:
        action = "Updated"

    user = instance if hasattr(instance, 'is_authenticated') and instance.is_authenticated else None
    AuditLog.objects.create(
        user=user,
        action=action,
        content_type=ContentType.objects.get_for_model(sender),
        object_id=instance.id,
    )

@receiver(pre_delete)
def create_audit_log_on_delete(sender, instance, **kwargs):
    if sender == AuditLog or sender == MyCounter or sender == Session:
        return

    action = "Deleted"

    user = instance if hasattr(instance, 'is_authenticated') and instance.is_authenticated else None

    AuditLog.objects.create(
        user=user,
        action=action,
        content_type=ContentType.objects.get_for_model(sender),
        object_id=instance.id,
    )


def validate_model_name(app_name, value):
    if app_name and value:
        app_models = get_sub_app_models(get_current_app_name())
        if value not in app_models:
            raise ValidationError(f'There is no {value} model in {app_name} application')
       
class Classification(CommonModel):

    app = models.CharField(max_length=50, verbose_name="Application", null=True, blank=True, choices=get_app_names)
    model = models.CharField(max_length=40, verbose_name="Model Name", null=True, blank=True) # Represents destination model.
    name = models.CharField(max_length=100, verbose_name="Classifications Name") # Name for this classification.
    sub_class = models.CharField(max_length=100, verbose_name="Sub Classifications Name", null=True, blank=True) # Sub Name for this classification.
    type = models.CharField(max_length=100, verbose_name="Type of Classification") # Grand type classifing subject.
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return f"{self.app}, {self.model}, {self.name}- {self.type}"

    def clean(self):
        super().clean()
        app_name = self.app
        model_name = self.model

        # Checking inserted model validation in the selected application
        validate_model_name(app_name, model_name)

class Location(CommonModel):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Longitude", blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Latitude", blank=True, null=True)
    gps_longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="GPS Longitude", null=True, blank=True)
    gps_latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="GPS Latitude", null=True, blank=True)

    def __str__(self):
        return self.name


class JobRoles(models.Model):
    name = models.CharField(verbose_name="Role Name", max_length=100)
    description = models.TextField(verbose_name="Description")
    Jobs = models.ManyToManyField('Jobs', blank=True)

    def __str__(self):
        return self.name

class Jobs(models.Model):
    role = models.ForeignKey(JobRoles, on_delete=models.CASCADE, verbose_name="Related Role")
    name = models.CharField(verbose_name="Job Name", max_length=100)
    description = models.TextField(verbose_name="Description")


class DateSlot(CommonModel):
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"

class TimeSlot(CommonModel):
    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Time")

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

class Schedule(CommonModel):
    classification = models.ManyToManyField(Classification, related_name="schedule")
    dates = models.ForeignKey(DateSlot, on_delete=models.CASCADE, verbose_name="Dates")
    times = models.ManyToManyField(TimeSlot, verbose_name="Times")

    def __str__(self):
        return f"Schedule {self.pk}"


class Document(CommonModel):
    title = models.CharField(max_length=100, verbose_name="Title")
    document = models.FileField(upload_to="documents/pdf", verbose_name="Document")
    image = models.FileField(upload_to="documents/img", verbose_name="Picture")
    description = models.CharField(max_length=255, blank=True, verbose_name="Description")

    def __str__(self):
        return self.description    


class TokenLifetime(CommonModel):
    lifetime = models.DurationField()

    def clean(self):
        if isinstance(self.lifetime, str):
            match = re.match(r'(\d+):(\d+):(\d+)', self.lifetime)
            if match:
                hours, minutes, seconds = map(int, match.groups())
                self.lifetime = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            else:
                raise ValidationError({
                    'lifetime': ValidationError(
                        'Lifetime must be a string in the format HH:MM:SS or a valid timedelta object.',
                        code='invalid'
                    )
                })
        elif not isinstance(self.lifetime, timedelta):
            raise ValidationError({
                'lifetime': ValidationError(
                    'Lifetime must be a string in the format HH:MM:SS or a valid timedelta object.',
                    code='invalid'
                )
            })

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.lifetime)

class User(AbstractUser, CommonModel):
    token_lifetime = models.ForeignKey(TokenLifetime, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name="User Description")

    def __str__(self):
        return self.username

class UserProfile(CommonModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    mobile_number = models.CharField(max_length=15)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='cover_images/', blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    following = models.ManyToManyField(User, related_name='followers', blank=True)

    def __str__(self):
        return self.user.username + "'s Profile"

    # def save(self, *args, **kwargs):
    #     if self.user is not None:
    #     existing_profiles = UserProfile.objects.filter(user=self.user.id, deleted_at__isnull=False)
    #     if existing_profiles.exists():
    #         for profile in existing_profiles:
    #             fields_to_exclude = ['id', 'created_at', 'updated_at', 'deleted_at']
    #             fields_to_update = self._meta.fields.exclude(name__in=fields_to_exclude)
    #             for field in fields_to_update:
    #                 setattr(profile, field.name, getattr(self, field.name))
    #             profile.deleted_at = None
    #             profile.save()
    #     else:
    #         super().save(*args, **kwargs)
            

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    reason = models.CharField(max_length=255, null=True, blank=True)

    
class Person(CommonModel):
    SEX = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="person")
    firstname = models.TextField(db_column="firstname", verbose_name="First Name", null=True) #CharField(max_length=336+16*40, db_column='firstname', null=True)
    lastname = models.TextField(db_column="lastname", verbose_name="Last Name", null=True) #CharField(max_length=336+16*60, db_column="lastname", null=True)
    date_of_birth = models.CharField(max_length=10, db_column="birthdate", verbose_name="Birthdate", null=True) #CharField(max_length=336+16*18, db_column="birthdate", null=True)
    national_code = models.TextField(db_column="national_code", verbose_name="National Code", null=True) #CharField(max_length=336+16*10, db_column="national_code", null=True)
    ssn = models.CharField(max_length=366*16*12, null=True) # Social Security Number 
    passport_number = models.TextField(db_column="passport_number", verbose_name="Passport Number", null=True) #CharField(max_length=336+16*10, db_column="passport_number", null=True)
    gender = models.CharField(max_length=336+16*10, choices=SEX, db_column="gender", verbose_name="Gender", null=True)
    mobile_phone = PhoneNumberField(unique=True, blank=True, null=True,) #CharField(max_length=336+16*20, db_column="mobile_phone", null=True)
    email = models.EmailField(db_column="email", verbose_name='email address', max_length=255, unique=True, blank=True, null=True,)
    website = models.URLField(blank=True, null=True, verbose_name="Website Address")
    nationality = models.TextField(db_column="nationality", verbose_name="Nationality", null=True)
    pictures = models.ManyToManyField('Pictures', blank=True, related_name="person")
    address = models.ManyToManyField('Places', through='PersonPlace', related_name="place_manager", blank=True) #models.TextField(db_column="address", verbose_name="Address", null=True) #CharField(max_length=336+16*100, null=True, db_column="address", blank=True)
    jobs = models.ManyToManyField(Jobs, verbose_name="Jobs")
    bio = models.TextField(verbose_name="About Me", null=True, blank=True)

    def __str__(self):
        return f"{self.id}- {self.firstname} {self.lastname}"

    class Meta:
        # ordering = []
        unique_together = ['nationality', 'national_code']


    # @property
    # def firstname(self):
    #     return decoder(self._firstname)
    # @property
    # def lastname(self):
    #     return decoder(self._lastname)
    # @property
    # def date_of_birth(self):
    #     return decoder(self._date_of_birth)
    # @property
    # def national_code(self):
    #     return decoder(self._national_code)
    # @property
    # def ssn(self):
    #     return decoder(self._ssn)
    # @property
    # def passport_number(self):
    #     return decoder(self._passport_number)
    # @property
    # def gender(self):
    #     return decoder(self._gender)
    # @property
    # def mobile_phone(self):
    #     return decoder(self._mobile_phone)
    # @property
    # def email(self):
    #     return decoder(self._email)
    # @property
    # def website(self):
    #     return decoder(self._website)
    # @property
    # def nationality(self):
    #     return decoder(self._nationality)
    # @property
    # def profile_picture(self):
    #     return decoder(self._profile_picture)

    # @firstname.setter
    # def firstname(self, value):
    #     self._firstname = value
    # @lastname.setter
    # def lastname(self, value):
    #     self._lastname = value
    # @date_of_birth.setter
    # def date_of_birth(self, value):
    #     self._date_of_birth = value
    # @national_code.setter
    # def national_code(self, value):
    #     self._national_code = value
    # @ssn.setter
    # def ssn(self, value):
    #     self._ssn = value
    # @passport_number.setter
    # def passport_number(self, value):
    #     self._passport_number = value
    # @gender.setter
    # def gender(self, value):
    #     self._gender = value
    # @mobile_phone.setter
    # def mobile_phone(self, value):
    #     self._mobile_phone = value
    # @email.setter
    # def email(self, value):
    #     self._email = value
    # @website.setter
    # def website(self, value):
    #     self._website = value
    # @nationality.setter
    # def nationality(self, value):
    #     self._nationality = value
    # @profile_picture.setter
    # def profile_picture(self, value):
    #     self._profile_picture = value

    # def save(self, *args, **kwargs):
    #     self.firstname = encoder(self.firstname)
    #     self.lastname = encoder(self.lastname)
        # self.date_of_birth = encoder(self.date_of_birth)
        # self.national_code = encoder(self.national_code)
        # self.ssn = encoder(self.ssn)
        # self.passport_number = encoder(self.passport_number)
        # self.gender = encoder(self.gender)
        # self.mobile_phone = encoder(self.mobile_phone)
        # self.email = encoder(self.email)
        # self.website = encoder(self.website)
        # self.nationality = encoder(self.nationality)
        # self.profile_picture = encoder(self.profile_picture)
        # super(Person, self).save(*args, **kwargs)


class Places(CommonModel):
    _title = models.CharField(max_length=366+16*50, db_column="title", verbose_name="Title", null=True)
    _country = models.CharField(max_length=366+16*20, db_column="country", null=True, verbose_name="Country")
    _statee = models.CharField(max_length=366+16*20, db_column="state", null=True, verbose_name="State")
    _city = models.CharField(max_length=366+16*20, db_column="city", null=True, verbose_name="City")
    _address = models.CharField(max_length=366+16*100, db_column="address", null=True, verbose_name="Address")
    _postalcode = models.CharField(max_length=366+16*15, db_column="postalcode", null=True, verbose_name="Postalcode")
    _phoneNumber = models.CharField(max_length=366+16*15, db_column="phone_number", null=True, verbose_name="Phone Number")
    website = models.URLField(blank=True, null=True, verbose_name="Website Address")
    _usage = models.TextField(db_column="usage", verbose_name="Usage", null=True)
    _area = models.CharField(max_length=366+16*11, db_column="area", verbose_name="Area", null=True, blank=True)
    _num_floors = models.CharField(max_length=366+16*3, db_column="num_floors", verbose_name="Number Floors", null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, related_name="place", verbose_name="Location", null=True)
    manager = models.ForeignKey(Person, on_delete=models.SET_NULL,  db_column="manager", related_name="manager_place", verbose_name="Manager", null=True, blank=True)

    def __str__(self):
        return f"{self.id}- {self.title}"
    
    @property
    def title(self):
        return decoder(self._title)
    @property
    def country(self):
        return decoder(self._country)
    @property
    def state(self):
        return decoder(self._statee)
    @property
    def city(self):
        return decoder(self._city)
    @property
    def address(self):
        return decoder(self._address)
    @property
    def postalcode(self):
        return decoder(self._postalcode)
    @property
    def phoneNumber(self):
        return decoder(self._phoneNumber)
    @property
    def usage(self):
        return decoder(self._usage)
    @property
    def area(self):
        return decoder(self._area)
    @property
    def num_floors(self):
        return decoder(self._num_floors)

    @title.setter
    def title(self, value):
        self._title = value
    @country.setter
    def country(self, value):
        self._country = value
    @state.setter
    def state(self, value):
        self._statee = value
    @city.setter
    def city(self, value):
        self._city = value
    @address.setter
    def address(self, value):
        self._address = value
    @postalcode.setter
    def postalcode(self, value):
        self._postalcode = value
    @phoneNumber.setter
    def phoneNumber(self, value):
        self._phoneNumber = value
    @usage.setter
    def usage(self, value):
        self._usage = value
    @area.setter
    def area(self, value):
        self._area = value
    @num_floors.setter
    def num_floors(self, value):
        self._num_floors = value

    def save(self, *args, **kwargs):
        self.title = encoder(self.title)
        self.country = encoder(self.country)
        self.state = encoder(self.state)
        self.city = encoder(self.title)
        self.address = encoder(self.address)
        self.postalcode = encoder(self.postalcode)
        self.phoneNumber = encoder(self.phoneNumber)
        self.usage = encoder(self.usage)
        self.area = encoder(self.area)
        self.num_floors = encoder(self.num_floors)
        super(Places, self).save(*args, **kwargs)

        
class PersonPlace(CommonModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="person_place")
    place = models.ForeignKey(Places, on_delete=models.CASCADE, related_name="place_person")
    _priority = models.CharField(max_length=366+16*3, db_column="priority", verbose_name="Priority", null=True)
    _role = models.CharField(max_length=366+16*20, db_column="role", verbose_name="Role and Position", null=True)
    _responsibility = models.TextField(db_column="responsibility", verbose_name="Responsibility", null=True)
    website = models.URLField(blank=True, null=True, verbose_name="آدرس وبسایت")

    def __str__(self):
        return f"{self.person.lastname} - {self.place.title}"

    @property
    def priority(self):
        return decoder(self._priority)
    @property
    def role(self):
        return decoder(self._role)
    @property
    def responsibility(self):
        return decoder(self._responsibility)

    @priority.setter
    def priority(self, value):
        self._priority = value
    @role.setter
    def role(self, value):
        self._role = value
    @responsibility.setter
    def responsibility(self, value):
        self._responsibility = value

    def save(self, *args, **kwargs):
        self.priority = encoder(self.priority)
        self.role = encoder(self.role)
        self.responsibility = encoder(self.responsibility)
        super(PersonPlace, self).save(*args, **kwargs)


# نوع شخصیت‌های حقوقی
    # LEGAL_ENTITY_TYPES = [
    #     ('company', 'Company'),
    #     ('organization', 'Organization'),
    #     ('institution', 'Institution'),
    # ]
class LegalTypes(CommonModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class LegalEntity(CommonModel):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(LegalTypes, on_delete=models.CASCADE, related_name="legal_entity")
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, related_name="legal_entity", null=True)
    registration_number = models.CharField(max_length=50, unique=True)
    address = models.ManyToManyField(Places, related_name="legal_entity", through="LegalEntityPlaces")
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# Through model↓
class LegalEntityPlaces(CommonModel):
    legalentity = models.ForeignKey(LegalEntity, on_delete=models.CASCADE, related_name="through")
    places = models.ForeignKey(Places, on_delete=models.CASCADE, related_name="throught")
    order = models.PositiveSmallIntegerField()
    usage = models.CharField(max_length=128, null=True)
    descrition = models.TextField()


class University(CommonModel):
    name = models.CharField(max_length=200, verbose_name="University Name")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, verbose_name="Geographical Location", null=True)
    places = models.ManyToManyField(Places, through="UniversityPlaces", related_name="university")
    website = models.URLField(verbose_name="Website Address")

    def __str__(self):
        return self.name

class UniversityPlaces(CommonModel):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="university_places")
    places = models.ForeignKey(Places, on_delete=models.CASCADE, related_name="university_places")
    name = models.CharField(max_length=80, verbose_name="University region Name")
    type = models.ForeignKey(Classification, on_delete=models.SET_NULL, related_name="university_places", null=True)
    description = models.TextField()


class FieldOfStudy(CommonModel):
    name = models.CharField(max_length=200, verbose_name="Field of Study Name", unique=True)
    classification = models.ForeignKey(Classification, related_name="field_of_study", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="نوع رشته تحصیلی")
    description = models.TextField(verbose_name="Description")

    def __str__(self):
        return self.name
    # CATEGORY_CHOICES = [
    #     ('General', 'عمومی'),
    #     ('Specialty', 'تخصصی'),
    #     ('Subspecialty', 'فوق تخصصی'),
    #     ('Fellowship', 'فلوشیپ'),
    # ]


class AcademicCategory(CommonModel):
    name = models.CharField(max_length=20, unique=True, verbose_name="Category Name")
    description = models.TextField(verbose_name="Description")

    def __str__(self):
        return self.name
# ایجاد دسته‌بندی‌های علمی
# academic_category1 = AcademicCategory.objects.create(name="دانشجو")
# academic_category2 = AcademicCategory.objects.create(name="استادیار")
# academic_category3 = AcademicCategory.objects.create(name="استاد")
# دسته‌بندی‌های علمی "عمومی"، "تخصصی"، "فوق تخصصی"، "فلوشیپ" 


class AcademicRank(CommonModel):
    name = models.CharField(max_length=200, verbose_name="Academic Rank Name", unique=True)
    description = models.TextField(verbose_name="Description")
    # field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.SET_NULL, related_name="academic_rank", verbose_name="رشته تحصیلی", null=True, blank=True)
    # duration_years = models.PositiveIntegerField(verbose_name="مدت زمان (سال)", null=True, blank=True)

    def __str__(self):
        return self.name
# ایجاد ترتیب‌های علمی
# academic_rank1 = AcademicRank.objects.create(name="دانشجوی دکتری")
# academic_rank2 = AcademicRank.objects.create(name="استادیار")
# academic_rank3 = AcademicRank.objects.create(name="دانشیار")
# academic_rank4 = AcademicRank.objects.create(name="استاد")
#  ترتیب‌های علمی "دانشجو"، "استادیار"، "استاد"


class EducationalDegree(CommonModel):
    name = models.CharField(max_length=200, verbose_name="Educational Degree Name", unique=True)
    abbreviation = models.CharField(max_length=100, verbose_name="Degree Abbreviation")
    description = models.TextField(verbose_name="Description")
    duration_years = models.PositiveIntegerField(verbose_name="Duration (Years)")
    # academic_rank = models.ForeignKey(AcademicRank, on_delete=models.CASCADE, verbose_name="رتبه علمی", null=True, blank=True)
    # category = models.ForeignKey(AcademicCategory, on_delete=models.PROTECT, verbose_name="دسته بندی", null=True, blank=True)

    def __str__(self):
        return self.name


class AcademicRecord(CommonModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Person")
    university = models.ForeignKey(University, on_delete=models.CASCADE, verbose_name="University")
    academic_category = models.ForeignKey(AcademicCategory, on_delete=models.CASCADE, verbose_name="Academic Category")
    academic_rank = models.ForeignKey(AcademicRank, on_delete=models.CASCADE, verbose_name="Academic Rank")
    field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE, verbose_name="Field of Study")
    medical_degree = models.ForeignKey(EducationalDegree, on_delete=models.CASCADE, verbose_name="Degree")
    graduation_year = models.PositiveIntegerField(verbose_name="Graduations Year")
    gpa = models.FloatField(verbose_name="GPA")

    def __str__(self):
        return f"{self.person_name} - {self.field_of_study}"


class LoginRecord(CommonModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="User", null=True)
    ipv4_address = models.GenericIPAddressField(protocol='IPv4', verbose_name="IPv4 Address", blank=True, null=True)
    ipv6_address = models.GenericIPAddressField(protocol='IPv6', verbose_name="IPv6 Address", blank=True, null=True)
    ip_validation_status = models.CharField(max_length=255, null=True, blank=True)
    login_date_time = models.DateTimeField(verbose_name="Login Date and Time")
    user_agent_data = models.TextField(null=True, blank=True)
    device_type = models.CharField(max_length=100, null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL, related_name="login_record", verbose_name="Location")
    gps_location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL, related_name="gps_login_record", verbose_name="GPS Location")


    def __str__(self):
        return f"{self.user.username} - {self.login_date_time}"


class UserSession(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    session_key = models.CharField(max_length=40, unique=True, verbose_name="Session Key")
    session_data = models.TextField(verbose_name="Session Data")
    login_time = models.DateTimeField(auto_now_add=True, verbose_name="Login Time")
    logout_time = models.DateTimeField(null=True, blank=True, verbose_name="Logout Time")
    device_type = models.CharField(max_length=100, null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL, related_name="user_session", verbose_name="Location")

    def __str__(self):
        return f"{self.user.username} - {self.session_key}"


class SiteManagementLog(CommonModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="site_management", verbose_name="User", null=True)
    _ip4 = models.CharField(max_length=366+16*12, db_column="ip4", verbose_name="IP4", null=True)
    _ip6 = models.CharField(max_length=366+16*39, db_column="ip6", verbose_name="IP6", null=True)
    _link = models.TextField(db_column="link", verbose_name="Link", null=True)
    _action = models.TextField(db_column="action", verbose_name="Action", null=True)

    @property
    def ip4(self):
        return decoder(self._ip4)
    @property
    def ip6(self):
        return decoder(self._ip6)
    @property
    def link(self):
        return decoder(self._link)
    @property
    def action(self):
        return decoder(self._action)

    @ip4.setter
    def ip4(self, value):
        self._ip4 = value
    @ip6.setter
    def ip6(self, value):
        self._ip6 = value
    @link.setter
    def link(self, value):
        self._link = value
    @action.setter
    def action(self, value):
        self._action = value

    def save(self, *args, **kwargs):
        self.ip4 = encoder(self.ip4)
        self.ip6 = encoder(self.ip6)
        self.link = encoder(self.link)
        self.action = encoder(self.action)
        super(SiteManagementLog, self).save(*args, **kwargs)


class SchedulePlan(CommonModel):
    traveler = models.ForeignKey(Person, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.SET_NULL, related_name="schedule_plan", null=True)
    airline_ticket = models.CharField(max_length=100, null=True, blank=True)
    hotel_reservation = models.CharField(max_length=100, null=True, blank=True)
    other_details = models.TextField(null=True, blank=True)
    model_documentation = models.ManyToManyField(Document, related_name="common_schedule_plan")

    def __str__(self):
        return f"{self.traveler.name}'s Schedule Plan"


class Survey(CommonModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Question(CommonModel):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.TextField()
    is_required = models.BooleanField(default=True)

    def __str__(self):
        return self.text

class Answer(CommonModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    respondent_name = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="answer")
    response = models.TextField()

    def __str__(self):
        return f"{self.question.text} - {self.respondent_name}"


class Rating(CommonModel):
    title = models.CharField(max_length=100)
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, related_name="common_rating", null=True)
    rating = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])
    review = models.TextField()
    rater_name = models.ForeignKey(Person, on_delete=models.SET_NULL, related_name="rating", null=True)

    def __str__(self):
        return f"{self.rater_name} to {self.title},  {self.rating} Scores gain"


class Translate(CommonModel):
    persian = models.TextField(null=True, blank=True)
    english = models.TextField(null=True, blank=True)
    arabic = models.TextField(null=True, blank=True)
    russian = models.TextField(null=True, blank=True)
    chineseTraditional = models.TextField(null=True, blank=True)
    spanish = models.TextField(null=True, blank=True)
    french = models.TextField(null=True, blank=True)
    german = models.TextField(null=True, blank=True)
    italian = models.TextField(null=True, blank=True)


def default_allowed_image_formats():
    return ['jpg', 'png', 'jpeg']

class SystemSettingsPic(CommonModel):
    settings_pic = [
        ('swiper', 'Swiper'),
        ('prfpic', 'Profile Picture'),
        ('cflag', 'Contry Flag'),
    ]
    company = models.ForeignKey('administration.Company', on_delete=models.CASCADE, related_name="system_settings_pic", null=True)
    app = models.CharField(max_length=50, choices=get_app_names, null=True, blank=True)
    name = models.CharField(max_length=30, choices=settings_pic, null=True, blank=True)
    max_image_size_width = models.PositiveIntegerField(verbose_name='Max Image Size Width', default=1200)
    max_image_size_height = models.PositiveIntegerField(verbose_name='Max Image Size Height', default=800)
    max_image_file_size_mb = models.PositiveIntegerField(
        verbose_name='Max Image File Size (MB)',
        default=2,
        help_text='Enter the maximum image file size in megabytes (MB).'
    )
    @property
    def max_image_file_size_bytes(self):
        return self.max_image_file_size_mb * 1024 * 1024
        
    allowed_image_formats = models.JSONField(
        verbose_name='Allowed Image Formats', 
        default=default_allowed_image_formats,
    )

    class Meta:
        unique_together = [['app', 'name']]  

    def __str__(self):
        return f"{self.app} System Settings, {self.name}"


class Pictures(CommonModel):
    image_settings = models.ForeignKey(SystemSettingsPic, on_delete=models.CASCADE, related_name="pictures")
    classification = models.ManyToManyField(Classification, blank=True, related_name="picture")
    name = models.CharField(max_length=20, null=True, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to='images/',
        null=True,
        blank=True,
        max_length=255,  # حداکثر طول مسیر ذخیره شده در پایگاه داده
        height_field='image_height',  # فیلد مربوط به ارتفاع تصویر
        width_field='image_width',  # فیلد مربوط به عرض تصویر
    )
    image_width = models.PositiveIntegerField(null=True, blank=True, default='image_width')
    image_height = models.PositiveIntegerField(null=True, blank=True, default='image_width')

    def save(self, *args, **kwargs):
        # از مقادیر مدل ImageSettings استفاده می‌کنیم
        max_upload_size = self.image_settings.max_image_file_size_bytes
        formats = self.image_settings.allowed_image_formats
        max_image_size = (self.image_settings.max_image_size_width, self.image_settings.max_image_size_height)

        # اختصاص مقادیر به فیلد image
        self.image.max_upload_size = max_upload_size  # حداکثر حجم فایل
        self.image.formats = formats  # فرمت‌های مجاز
        
        if not self.pk:  # بررسی برای ایجاد
            # تولید نام منحصر به فرد برای فایل جدید
            self.image.name = generate_unique_image_filename(self.image)
            # ذخیره تصویر با استفاده از متد save از والدین ImageField
            self.image.save(self.image.name, self.image.file, save=False)
        
        super(Pictures, self).save(*args, **kwargs)

        if self.image:
        # Open the image and get its width
            with Image.open(self.image.path) as img:
                self.image_width = img.width
                self.image_height = img.height
                # Save the model again with updated image_width
                super().save(update_fields=['image_width', 'image_height'])
    
# تابع برای حذف فایل پس از حذف مدل
@receiver(post_delete, sender=Pictures)
def delete_picture(sender, instance, **kwargs):
    if instance.image:
        # ایجاد مسیر موردنیاز
        destination = 'temp/' + instance.image.name.split('/')[-1]
        
        # بررسی وجود پوشه و ایجاد آن در صورت لزوم
        if not os.path.exists('temp'):
            os.makedirs('temp')
        
        # منتقل کردن فایل به مسیر موردنظر
        shutil.move(instance.image.path, destination)

def get_templates(app_name):
    app = apps.get_app_config(app_name)
    return [(t.name, t.name) for t in app.get_template_names()]

def validate_level(value):
    parts = value.split('-')
    for part in parts:
        try:
            int(part)
        except ValueError:
            raise ValidationError("Should be separated with -")


class AppModels(CommonModel):
    application = models.CharField(max_length=50, choices=get_app_names)
    model = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.application}: {self.model}"
    
    class Meta:
        unique_together=['application', 'model']

    def clean(self):
        if not self.model in get_sub_app_models(self.application):
            raise ValidationError("Inserted model is not defined in the selected application!")

    def get_related_model(self):
        # pdb.set_trace()
        return apps.get_model(self.application, self.model)            

class Setting(CommonModel):
    company = models.ForeignKey('administration.Company', on_delete=models.CASCADE, related_name="setting_menus", null=True)
    application = models.CharField(max_length=50, choices=get_app_names)
    page = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.company}, {self.application}, {self.page}, {self.model}"

class SettingMenus(CommonModel):
    TAG =(
        ("div", "div"),
        ("section", "section"),
        ("article", "article"),
        ('', '')
    )
    cat = models.ForeignKey(Setting, on_delete=models.CASCADE, related_name="menus", null=True)
    index = models.SmallIntegerField(validators=[MaxValueValidator(32766)], default=0)
    name = models.CharField(max_length=100, null=True)
    path = models.CharField(max_length=200, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='sub_categories', on_delete=models.CASCADE)
    role = models.ManyToManyField(UserRole, related_name="settingMenus", blank=True)
    individual_permission = models.ManyToManyField(Permission, related_name="setting_menus", blank = True)
    tables = models.ManyToManyField(AppModels, related_name="setting_menus", blank = True,)
    container_tag = models.CharField(max_length=15, null=True, choices=TAG)
    is_active = models.BooleanField(default=True)
    url = models.URLField(blank=True, null=True, verbose_name="Website Address")
    order = models.IntegerField(db_index=True)

    def __str__(self):
        return f"{self.index}, {self.name}"

    class Meta:
        ordering = ['cat', 'index']
        unique_together = ['cat', 'index', 'name', 'parent', 'deleted_at']

    def clean(self):
        super().clean()
        if self.cat and self.index is not None and self.name:
            duplicates = SettingMenus.objects.filter(
                cat=self.cat,
                index=self.index,
                name=self.name,
                parent=self.parent
            ).exclude(pk=self.pk)
            if duplicates.exists():
                raise ValidationError("Duplicate record found.")

    def has_access(self, user):
        if user.groups.filter(name=user.username).exists():
            return True
        else:
            return False    


class MyCounter(models.Model):
    name = models.CharField(max_length=20, default="default")
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class DynamicTableTest1(CommonModel):
    SEX = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    )
    firstname = models.TextField(db_column="firstname", verbose_name="First Name", null=True)
    lastname = models.TextField(db_column="lastname", verbose_name="Last Name", null=True)
    date_of_birth = models.CharField(max_length=10, db_column="birthdate", verbose_name="Birthdate", null=True)
    national_code = models.TextField(db_column="national_code", verbose_name="National Code", null=True)
    ssn = models.CharField(max_length=12, null=True)
    passport_number = models.TextField(db_column="passport_number", verbose_name="Passport Number", null=True)
    gender = models.CharField(max_length=10, choices=SEX, db_column="gender", verbose_name="Gender", null=True)
    mobile_phone = PhoneNumberField(unique=True, blank=True, null=True,)
    email = models.EmailField(db_column="email", verbose_name='email address', max_length=255, unique=True, blank=True, null=True,)
    website = models.URLField(blank=True, null=True, verbose_name="Website Address")
    nationality = models.TextField(db_column="nationality", verbose_name="Nationality", null=True)
    pictures = models.ManyToManyField('Pictures', blank=True)
    address = models.ManyToManyField('Places', blank=True)
    jobs = models.ManyToManyField(Jobs, verbose_name="Jobs")
    bio = models.TextField(verbose_name="About Me", null=True, blank=True)

class DynamicTableTest2(CommonModel):
    SEX = (
    ('Male', 'مرد'),
    ('Female', 'زن'),
    )
    firstname = models.TextField(db_column="firstname", verbose_name="نام", null=True)
    lastname = models.TextField(db_column="lastname", verbose_name="نام خانوادگی", null=True)
    national_code = models.TextField(db_column="national_code", verbose_name="شماره ملی", null=True)
    date_of_birth = models.CharField(max_length=10, db_column="birthdate", verbose_name="تاریخ تولد", null=True)
    gender = models.CharField(max_length=10, choices=SEX, db_column="gender", verbose_name="جنسیت", null=True)    
    mobile_phone = PhoneNumberField(unique=True, verbose_name="شماره همراه", blank=True, null=True,)
    pictures = models.ManyToManyField('Pictures', blank=True, verbose_name="عکس")
    address = models.ManyToManyField('Places', blank=True, verbose_name="نشانی")
    jobs = models.ManyToManyField(Jobs, verbose_name="شغل")
    bio = models.TextField(verbose_name="توضیحات", null=True, blank=True)
