from django.contrib.auth.models import AbstractUser
from django.db import models
from common.utils.crypto import encoder, decoder

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

class Person(models.Model):
    SEX = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    id = models.AutoField(primary_key=True)
    # job1 = models.ForeignKey()
    # job_n = models.ForeignKey()
    firstname = models.CharField(max_length=64, null=True)
    lastname = models.CharField(max_length=80, null=True)
    birthdate = models.DateField(null=True)
    national_code = models.CharField(max_length=10, null=True)
    pasport_number = models.CharField(max_length=8, null=True)
    sex = models.CharField(max_length=10, choices=SEX, null=True)
    mobile_phone = models.CharField(max_length=15, null=True)
    address = models.ForeignKey('Places', null=True, on_delete=models.SET_NULL)
    createddtm = models.DateTimeField(auto_now_add=True)
    updatedtm = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField()

    @property
    def firstname(self):
        return decoder(self._firstname)

    @firstname.setter
    def firstname(self, value):
        self._firstname = value

    def save(self, *args, **kwargs):
        self._firstname=encoder(self._firstname)
        super(Person, self).save(*args, **kwargs)

class Places(models.Model):
    title = models.CharField(max_length=128)
    country = models.CharField(max_length=64, null=True)
    city = models.CharField(max_length=64, null=True)
    address = models.CharField(max_length=1024, null=True)
    usage = models.CharField(max_length=1024, null=True)
    createddtm = models.DateTimeField(auto_now_add=True)
    updatedtm = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField()
    