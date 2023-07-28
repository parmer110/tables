from django.db import models
from common.models import Person, Places, CommonModel

name  = "Colorectal Surgery"

class colorectal_surgery_Patient(models.Model):
    class Meta:
        db_table = 'colorectal_surgery_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class ColorectalSurgeryProcedure(models.Model):
    # فیلدهای مربوط به روش‌های جراحی پایین شکم
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی پایین شکم')
    description = models.TextField(verbose_name='توضیحات روش جراحی پایین شکم')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class ColorectalSurgeryTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های جراحی پایین شکم
    name = models.CharField(max_length=100, verbose_name='نام آزمایش جراحی پایین شکم')
    description = models.TextField(verbose_name='توضیحات آزمایش جراحی پایین شکم')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class colorectal_surgery_Treatment(models.Model):
    class Meta:
        db_table = 'colorectal_surgery_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(colorectal_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند جراحی پایین شکم
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    colorectal_surgery_procedures = models.ManyToManyField(ColorectalSurgeryProcedure, blank=True, verbose_name='روش‌های جراحی پایین شکم')
    colorectal_surgery_tests = models.ManyToManyField(ColorectalSurgeryTest, blank=True, verbose_name='آزمایش‌های جراحی پایین شکم')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی پایین شکم بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
