from django.db import models
from common.models import Person, Places, CommonModel

name = "Subspecialty Nuclear Medicine"

# مدل بیمار
class sub_nuclear_medicine_Patient(models.Model):
    class Meta:
        db_table = 'sub_nuclear_medicine_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

# مدل زیرتخصص پزشکی هسته‌ای (Nuclear Medicine)
class NuclearMedicine(models.Model):
    patient = models.ForeignKey(sub_nuclear_medicine_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    radioactive_isotopes = models.TextField(verbose_name='ایزوتوپ‌های رادیواکتیو')
    imaging_techniques = models.TextField(verbose_name='تکنیک‌های تصویربرداری')
    treatment_options = models.TextField(verbose_name='گزینه‌های درمانی هسته‌ای')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"زیرتخصص پزشکی هسته‌ای برای بیمار {self.patient.full_name}"

# مدل تجویز (sub_nuclear_medicine_Treatment)
class sub_nuclear_medicine_Treatment(models.Model):
    class Meta:
        db_table = 'sub_nuclear_medicine_Treatment'
    patient = models.ForeignKey(sub_nuclear_medicine_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    description = models.TextField(verbose_name='توضیحات تجویز')
    date = models.DateField(verbose_name='تاریخ تجویز')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"
