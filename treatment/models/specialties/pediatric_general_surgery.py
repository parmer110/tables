from django.db import models
from common.models import Person, Places, CommonModel

name = "Pediatric Plastic Surgery"

name = "Pediatric General Surgery"

class pediatric_general_surgery_Patient(models.Model):
    class Meta:
        db_table = 'pediatric_general_surgery_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class PediatricGeneralSurgeryProcedure(models.Model):
    # فیلدهای مربوط به روش‌های جراحی عمومی کودکان
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی عمومی کودکان')
    description = models.TextField(verbose_name='توضیحات روش جراحی عمومی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class PediatricGeneralSurgeryTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های جراحی عمومی کودکان
    name = models.CharField(max_length=100, verbose_name='نام آزمایش جراحی عمومی کودکان')
    description = models.TextField(verbose_name='توضیحات آزمایش جراحی عمومی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class pediatric_general_surgery_Treatment(models.Model):
    class Meta:
        db_table = 'pediatric_general_surgery_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(pediatric_general_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند جراحی عمومی کودکان
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    pediatric_general_surgery_procedures = models.ManyToManyField(PediatricGeneralSurgeryProcedure, blank=True, verbose_name='روش‌های جراحی عمومی کودکان')
    pediatric_general_surgery_tests = models.ManyToManyField(PediatricGeneralSurgeryTest, blank=True, verbose_name='آزمایش‌های جراحی عمومی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی عمومی کودکان بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
