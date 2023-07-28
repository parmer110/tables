from django.db import models
from common.models import Person, Places, CommonModel

name = "Pediatric Hematology"

class pediatric_hematology_Patient(models.Model):
    class Meta:
        db_table = 'pediatric_hematology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class PediatricHematologyProcedure(models.Model):
    # فیلدهای مربوط به روش‌های هماتولوژی کودکان
    name = models.CharField(max_length=100, verbose_name='نام روش هماتولوژی کودکان')
    description = models.TextField(verbose_name='توضیحات روش هماتولوژی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class PediatricHematologyTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های هماتولوژی کودکان
    name = models.CharField(max_length=100, verbose_name='نام آزمایش هماتولوژی کودکان')
    description = models.TextField(verbose_name='توضیحات آزمایش هماتولوژی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class pediatric_hematology_Treatment(models.Model):
    class Meta:
        db_table = 'pediatric_hematology_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(pediatric_hematology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند هماتولوژی کودکان
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    pediatric_hematology_procedures = models.ManyToManyField(PediatricHematologyProcedure, blank=True, verbose_name='روش‌های هماتولوژی کودکان')
    pediatric_hematology_tests = models.ManyToManyField(PediatricHematologyTest, blank=True, verbose_name='آزمایش‌های هماتولوژی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند هماتولوژی کودکان بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
