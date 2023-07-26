from django.contrib.auth.models import AbstractUser
from django.db import models
from common.utils.crypto import encoder, decoder

# Index:
    # CommonModel (Abstract)
    # User
    # Person
    # Place
    # SiteManagementsLog
class CommonModel(models.Model):
    id = models.AutoField(primary_key=True)
    createddtm = models.DateTimeField(auto_now_add=True, editable=False)
    updatedtm = models.DateTimeField(auto_now=True, editable=False)
    deleted = models.DateTimeField(null=True, editable=False)

    class Meta:
        abstract = True


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

class Person(CommonModel):
    SEX = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    _firstname = models.TextField(db_column="firstname", verbose_name="First Name", null=True) #CharField(max_length=336+16*40, db_column='firstname', null=True)
    _lastname = models.TextField(db_column="lastname", verbose_name="Last Name", null=True) #CharField(max_length=336+16*60, db_column="lastname", null=True)
    _birthdate = models.TextField(db_column="birthdate", verbose_name="Birthdate", null=True) #CharField(max_length=336+16*18, db_column="birthdate", null=True)
    _national_code = models.TextField(db_column="national_code", verbose_name="National Code", null=True) #CharField(max_length=336+16*10, db_column="national_code", null=True)
    _passport_number = models.TextField(db_column="passport_number", verbose_name="Passport Number", null=True) #CharField(max_length=336+16*10, db_column="passport_number", null=True)
    _sex = models.CharField(max_length=336+16*10, choices=SEX, db_column="sex", verbose_name="Sex", null=True)
    _mobile_phone = models.TextField(db_column="mobile_phone", verbose_name="Mobile Phone", null=True) #CharField(max_length=336+16*20, db_column="mobile_phone", null=True)
    _address = models.TextField(db_column="address", verbose_name="Address", null=True) #CharField(max_length=336+16*100, null=True, db_column="address", blank=True)

    def __str__(self):
        return f"{self.id}- {self.firstname} {self.lastname}"
    
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

class Places(CommonModel):
    _title = models.CharField(max_length=366+16*50, db_column="title", verbose_name="Title", null=True)
    _country = models.CharField(max_length=366+16*20, db_column="country", null=True, verbose_name="Country")
    _statee = models.CharField(max_length=366+16*20, db_column="state", null=True, verbose_name="State")
    _city = models.CharField(max_length=366+16*20, db_column="city", null=True, verbose_name="City")
    _address = models.CharField(max_length=366+16*100, db_column="address", null=True, verbose_name="Address")
    _postalcode = models.CharField(max_length=366+16*15, db_column="postalcode", null=True, verbose_name="Postalcode")
    _phoneNumber = models.CharField(max_length=366+16*15, db_column="phone_number", null=True, verbose_name="Phone Number")
    _usage = models.TextField(db_column="usage", verbose_name="Usage", null=True)
    manager = models.ForeignKey(Person, on_delete=models.CASCADE,  db_column="manager", related_name="Places", verbose_name="Manager", null=True)

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

    def save(self, *args, **kwargs):
        self.title = encoder(self.title)
        self.country = encoder(self.country)
        self.state = encoder(self.state)
        self.city = encoder(self.title)
        self.address = encoder(self.address)
        self.postalcode = encoder(self.postalcode)
        self.phoneNumber = encoder(self.phoneNumber)
        self.usage = encoder(self.usage)
        super(Places, self).save(*args, **kwargs)

        
class SiteManagementsLog(CommonModel):
    _ip4 = models.CharField(max_length=366+16*12, db_column="ip4", verbose_name="IP4", null=True)
    _ip6 = models.CharField(max_length=366+16*39, db_column="ip6", verbose_name="IP6", null=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="SiteManagementsLog", db_column="person", verbose_name="Person", null=True)
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
        super(SiteManagementsLog, self).save(*args, **kwargs)
