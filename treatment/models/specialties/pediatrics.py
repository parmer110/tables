from django.db import models
from common.models import Person, Places, CommonModel

name="Pediatrics"

class pediatrics_Patient(models.Model):
    class Meta:
        db_table = 'pediatrics_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class PediatricProcedure(models.Model):
    # فیلدهای مربوط به روش‌های پزشکی کودکان
    name = models.CharField(max_length=100, verbose_name='نام روش پزشکی کودکان')
    description = models.TextField(verbose_name='توضیحات روش پزشکی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class PediatricTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های پزشکی کودکان
    name = models.CharField(max_length=100, verbose_name='نام آزمایش پزشکی کودکان')
    description = models.TextField(verbose_name='توضیحات آزمایش پزشکی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class pediatrics_Treatment(models.Model):
    class Meta:
        db_table = 'pediatrics_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(pediatrics_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند پزشکی کودکان
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    pediatric_procedures = models.ManyToManyField(PediatricProcedure, blank=True, verbose_name='روش‌های پزشکی کودکان')
    pediatric_tests = models.ManyToManyField(PediatricTest, blank=True, verbose_name='آزمایش‌های پزشکی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند پزشکی کودکان بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
