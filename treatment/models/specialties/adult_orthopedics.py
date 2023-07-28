from django.db import models
from common.models import Person, Places, CommonModel

name = "Adult Orthopedics"

class adult_orthopedics_Patient(models.Model):
    class Meta:
        db_table = 'adult_orthopedics_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class AdultOrthopedicsProcedure(models.Model):
    # فیلدهای مربوط به روش‌های ارتوپدی بالغین
    name = models.CharField(max_length=100, verbose_name='نام روش ارتوپدی بالغین')
    description = models.TextField(verbose_name='توضیحات روش ارتوپدی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class AdultOrthopedicsTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های ارتوپدی بالغین
    name = models.CharField(max_length=100, verbose_name='نام آزمایش ارتوپدی بالغین')
    description = models.TextField(verbose_name='توضیحات آزمایش ارتوپدی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class adult_orthopedics_Treatment(models.Model):
    class Meta:
        db_table = 'adult_orthopedics_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(adult_orthopedics_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند ارتوپدی بالغین
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    adult_orthopedics_procedures = models.ManyToManyField(AdultOrthopedicsProcedure, blank=True, verbose_name='روش‌های ارتوپدی بالغین')
    adult_orthopedics_tests = models.ManyToManyField(AdultOrthopedicsTest, blank=True, verbose_name='آزمایش‌های ارتوپدی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند ارتوپدی بالغین بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
