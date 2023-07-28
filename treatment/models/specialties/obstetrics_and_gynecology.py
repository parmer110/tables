from django.db import models
from common.models import Person, Places, CommonModel

name = "Obstetrics and Gynecology"

class obstetrics_and_gynecology_Patient(models.Model):
    class Meta:
        db_table = 'obstetrics_and_gynecology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class ObstetricsProcedure(models.Model):
    # فیلدهای مربوط به روش‌های زنان و زایمان
    name = models.CharField(max_length=100, verbose_name='نام روش زنان و زایمان')
    description = models.TextField(verbose_name='توضیحات روش زنان و زایمان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class GynecologyProcedure(models.Model):
    # فیلدهای مربوط به روش‌های زنانه
    name = models.CharField(max_length=100, verbose_name='نام روش زنانه')
    description = models.TextField(verbose_name='توضیحات روش زنانه')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class obstetrics_and_gynecology_Treatment(models.Model):
    class Meta:
        db_table = 'obstetrics_and_gynecology_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(obstetrics_and_gynecology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند زنان و زایمان
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    obstetrics_procedures = models.ManyToManyField(ObstetricsProcedure, blank=True, verbose_name='روش‌های زنان و زایمان')
    gynecology_procedures = models.ManyToManyField(GynecologyProcedure, blank=True, verbose_name='روش‌های زنانه')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند زنان و زایمان بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
