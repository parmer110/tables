from django.db import models
from common.models import Person, Places, CommonModel

name = "Pediatric Otolaryngology"

class pediatric_otolaryngology_Patient(models.Model):
    class Meta:
        db_table = 'pediatric_otolaryngology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class PediatricOtolaryngologyProcedure(models.Model):
    # فیلدهای مربوط به روش‌های گوش و حلق و بینی کودکان
    name = models.CharField(max_length=100, verbose_name='نام روش گوش و حلق و بینی کودکان')
    description = models.TextField(verbose_name='توضیحات روش گوش و حلق و بینی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class PediatricOtolaryngologyTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های گوش و حلق و بینی کودکان
    name = models.CharField(max_length=100, verbose_name='نام آزمایش گوش و حلق و بینی کودکان')
    description = models.TextField(verbose_name='توضیحات آزمایش گوش و حلق و بینی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class pediatric_otolaryngology_Treatment(models.Model):
    class Meta:
        db_table = 'pediatric_otolaryngology_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(pediatric_otolaryngology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند گوش و حلق و بینی کودکان
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    pediatric_otolaryngology_procedures = models.ManyToManyField(PediatricOtolaryngologyProcedure, blank=True, verbose_name='روش‌های گوش و حلق و بینی کودکان')
    pediatric_otolaryngology_tests = models.ManyToManyField(PediatricOtolaryngologyTest, blank=True, verbose_name='آزمایش‌های گوش و حلق و بینی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند گوش و حلق و بینی کودکان بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
