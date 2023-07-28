from django.db import models
from common.models import Person, Places, CommonModel

name = "Pediatric Orthopedics"

class pediatric_orthopedics_Patient(models.Model):
    class Meta:
        db_table = 'pediatric_orthopedics_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class PediatricOrthopedicsProcedure(models.Model):
    # فیلدهای مربوط به روش‌های ارتوپدی کودکان
    name = models.CharField(max_length=100, verbose_name='نام روش ارتوپدی کودکان')
    description = models.TextField(verbose_name='توضیحات روش ارتوپدی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class PediatricOrthopedicsTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های ارتوپدی کودکان
    name = models.CharField(max_length=100, verbose_name='نام آزمایش ارتوپدی کودکان')
    description = models.TextField(verbose_name='توضیحات آزمایش ارتوپدی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class pediatric_orthopedics_Treatment(models.Model):
    class Meta:
        db_table = 'pediatric_orthopedics_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(pediatric_orthopedics_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند ارتوپدی کودکان
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    pediatric_orthopedics_procedures = models.ManyToManyField(PediatricOrthopedicsProcedure, blank=True, verbose_name='روش‌های ارتوپدی کودکان')
    pediatric_orthopedics_tests = models.ManyToManyField(PediatricOrthopedicsTest, blank=True, verbose_name='آزمایش‌های ارتوپدی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند ارتوپدی کودکان بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
