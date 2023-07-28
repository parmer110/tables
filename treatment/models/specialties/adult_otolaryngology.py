from django.db import models
from common.models import Person, Places, CommonModel

name = "Adult Otolaryngology"

class adult_otolaryngology_Patient(models.Model):
    class Meta:
        db_table = 'adult_otolaryngology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class AdultOtolaryngologyProcedure(models.Model):
    # فیلدهای مربوط به روش‌های گوش و حلق و بینی بالغین
    name = models.CharField(max_length=100, verbose_name='نام روش گوش و حلق و بینی بالغین')
    description = models.TextField(verbose_name='توضیحات روش گوش و حلق و بینی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class AdultOtolaryngologyTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های گوش و حلق و بینی بالغین
    name = models.CharField(max_length=100, verbose_name='نام آزمایش گوش و حلق و بینی بالغین')
    description = models.TextField(verbose_name='توضیحات آزمایش گوش و حلق و بینی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class adult_otolaryngology_Treatment(models.Model):
    class Meta:
        db_table = 'adult_otolaryngology_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(adult_otolaryngology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند گوش و حلق و بینی بالغین
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    adult_otolaryngology_procedures = models.ManyToManyField(AdultOtolaryngologyProcedure, blank=True, verbose_name='روش‌های گوش و حلق و بینی بالغین')
    adult_otolaryngology_tests = models.ManyToManyField(AdultOtolaryngologyTest, blank=True, verbose_name='آزمایش‌های گوش و حلق و بینی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند گوش و حلق و بینی بالغین بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
