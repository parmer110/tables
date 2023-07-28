from django.db import models
from common.models import Person, Places, CommonModel

name = "Adult Gastroenterology"

class adult_gastroenterology_Patient(models.Model):
    class Meta:
        db_table = 'adult_gastroenterology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class GastroenterologyProcedure(models.Model):
    # فیلدهای مربوط به روش‌های گوارش بالغین
    name = models.CharField(max_length=100, verbose_name='نام روش گوارش بالغین')
    description = models.TextField(verbose_name='توضیحات روش گوارش بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class GastroenterologyTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های گوارش بالغین
    name = models.CharField(max_length=100, verbose_name='نام آزمایش گوارش بالغین')
    description = models.TextField(verbose_name='توضیحات آزمایش گوارش بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class adult_gastroenterology_Treatment(models.Model):
    class Meta:
        db_table = 'adult_gastroenterology_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(adult_gastroenterology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند گوارش بالغین
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    gastroenterology_procedures = models.ManyToManyField(GastroenterologyProcedure, blank=True, verbose_name='روش‌های گوارش بالغین')
    gastroenterology_tests = models.ManyToManyField(GastroenterologyTest, blank=True, verbose_name='آزمایش‌های گوارش بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند گوارش بالغین بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
