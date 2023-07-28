from django.db import models
from common.models import Person, Places, CommonModel

name="Internal Medicine"

class internal_medicine_Patient(models.Model):
    class Meta:
        db_table = 'internal_medicine_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class MedicalCondition(models.Model):
    # فیلدهای مربوط به بیماری‌های پزشکی داخلی
    name = models.CharField(max_length=100, verbose_name='نام بیماری')
    description = models.TextField(verbose_name='توضیحات بیماری')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Medication(models.Model):
    # فیلدهای مربوط به داروهای پزشکی داخلی
    name = models.CharField(max_length=100, verbose_name='نام دارو')
    description = models.TextField(verbose_name='توضیحات دارو')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class internal_medicine_Treatment(models.Model):
    class Meta:
        db_table = 'internal_medicine_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(internal_medicine_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند پزشکی داخلی
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    medical_conditions = models.ManyToManyField(MedicalCondition, blank=True, verbose_name='بیماری‌های پزشکی داخلی')
    medications = models.ManyToManyField(Medication, blank=True, verbose_name='داروهای مصرفی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند پزشکی داخلی بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
