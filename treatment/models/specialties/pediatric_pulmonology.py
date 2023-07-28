from django.db import models
from common.models import Person, Places, CommonModel

name = "Pediatric Pulmonology"

class pediatric_pulmonology_Patient(models.Model):
    class Meta:
        db_table = 'pediatric_pulmonology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class PediatricPulmonologyProcedure(models.Model):
    # فیلدهای مربوط به روش‌های ریه کودکان
    name = models.CharField(max_length=100, verbose_name='نام روش ریه کودکان')
    description = models.TextField(verbose_name='توضیحات روش ریه کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class PediatricPulmonologyTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های ریه کودکان
    name = models.CharField(max_length=100, verbose_name='نام آزمایش ریه کودکان')
    description = models.TextField(verbose_name='توضیحات آزمایش ریه کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class pediatric_pulmonology_Treatment(models.Model):
    class Meta:
        db_table = 'pediatric_pulmonology_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(pediatric_pulmonology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند ریه کودکان
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    pediatric_pulmonology_procedures = models.ManyToManyField(PediatricPulmonologyProcedure, blank=True, verbose_name='روش‌های ریه کودکان')
    pediatric_pulmonology_tests = models.ManyToManyField(PediatricPulmonologyTest, blank=True, verbose_name='آزمایش‌های ریه کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند ریه کودکان بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
