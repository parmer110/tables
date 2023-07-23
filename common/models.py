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
    _firstname = models.TextField(db_column="firstname", null=True) #CharField(max_length=336+16*40, db_column='firstname', null=True)
    _lastname = models.TextField(db_column="lastname", null=True) #CharField(max_length=336+16*60, db_column="lastname", null=True)
    _birthdate = models.TextField(db_column="birthdate", null=True) #CharField(max_length=336+16*18, db_column="birthdate", null=True)
    _national_code = models.TextField(db_column="national_code", null=True) #CharField(max_length=336+16*10, db_column="national_code", null=True)
    _passport_number = models.TextField(db_column="passport_number", null=True) #CharField(max_length=336+16*10, db_column="passport_number", null=True)
    _sex = models.CharField(max_length=336+16*10, choices=SEX, db_column="sex", null=True)
    _mobile_phone = models.TextField(db_column="mobile_phone", null=True) #CharField(max_length=336+16*20, db_column="mobile_phone", null=True)
    _address = models.TextField(db_column="address", null=True) #CharField(max_length=336+16*100, null=True, db_column="address", blank=True)
    createddtm = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedtm = models.DateTimeField(auto_now=True,null=True,  blank=True)
    deleted = models.DateTimeField()

    @property
    def firstname(self):
        return decoder(self._firstname)
    @property
    def lastname(self):
        return decoder(self._lastname)
    @property
    def birthdate(self):
        return decoder(self._birthdate)
    @property
    def national_code(self):
        return decoder(self._national_code)
    @property
    def passport_number(self):
        return decoder(self._passport_number)
    @property
    def sex(self):
        return decoder(self._sex)
    @property
    def mobile_phone(self):
        return decoder(self._mobile_phone)
    @property
    def address(self):
        return decoder(self._address)


    @firstname.setter
    def firstname(self, value):
        self._firstname = value
    @lastname.setter
    def lastname(self, value):
        self._lastname = value
    @birthdate.setter
    def birthdate(self, value):
        self._birthdate = value
    @national_code.setter
    def national_code(self, value):
        self._national_code = value
    @passport_number.setter
    def passport_number(self, value):
        self._passport_number = value
    @sex.setter
    def sex(self, value):
        self._sex = value
    @mobile_phone.setter
    def mobile_phone(self, value):
        self._mobile_phone = value
    @address.setter
    def address(self, value):
        self._address = value

    def save(self, *args, **kwargs):
        self.firstname = encoder(self.firstname)
        self.lastname = encoder(self.lastname)
        self.national_code = encoder(self.national_code)
        self.passport_number = encoder(self.passport_number)
        self.sex = encoder(self.sex)
        self.mobile_phone = encoder(self.mobile_phone)
        self.address = encoder(self.address)
        self.birthdate = encoder(self.birthdate)
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
    