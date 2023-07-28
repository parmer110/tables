from django.db import models
from common.models import Person, Places, CommonModel

name = "Vascular Surgery"

class vascular_surgery_Patient(models.Model):
    class Meta:
        db_table = 'vascular_surgery_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class VascularSurgeryProcedure(models.Model):
    # فیلدهای مربوط به روش‌های جراحی عروق
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی عروق')
    description = models.TextField(verbose_name='توضیحات روش جراحی عروق')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class VascularSurgeryTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های جراحی عروق
    name = models.CharField(max_length=100, verbose_name='نام آزمایش جراحی عروق')
    description = models.TextField(verbose_name='توضیحات آزمایش جراحی عروق')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class vascular_surgery_Treatment(models.Model):
    class Meta:
        db_table = 'vascular_surgery_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(vascular_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند جراحی عروق
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    vascular_surgery_procedures = models.ManyToManyField(VascularSurgeryProcedure, blank=True, verbose_name='روش‌های جراحی عروق')
    vascular_surgery_tests = models.ManyToManyField(VascularSurgeryTest, blank=True, verbose_name='آزمایش‌های جراحی عروق')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی عروق بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
