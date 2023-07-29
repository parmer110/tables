from django.db import models
from common.models import Person, Places, CommonModel

name = "Pediatric Gastroenterology"

class pediatric_gastroenterology_Patient(CommonModel):
    class Meta:
        db_table = 'pediatric_gastroenterology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class PediatricGastroenterologyProcedure(CommonModel):
    # فیلدهای مربوط به روش‌های گوارش کودکان
    name = models.CharField(max_length=100, verbose_name='نام روش گوارش کودکان')
    description = models.TextField(verbose_name='توضیحات روش گوارش کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class PediatricGastroenterologyTest(CommonModel):
    # فیلدهای مربوط به آزمایش‌های گوارش کودکان
    name = models.CharField(max_length=100, verbose_name='نام آزمایش گوارش کودکان')
    description = models.TextField(verbose_name='توضیحات آزمایش گوارش کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class pediatric_gastroenterology_Treatment(CommonModel):
    class Meta:
        db_table = 'pediatric_gastroenterology_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(pediatric_gastroenterology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند گوارش کودکان
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    pediatric_gastroenterology_procedures = models.ManyToManyField(PediatricGastroenterologyProcedure, blank=True, verbose_name='روش‌های گوارش کودکان')
    pediatric_gastroenterology_tests = models.ManyToManyField(PediatricGastroenterologyTest, blank=True, verbose_name='آزمایش‌های گوارش کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند گوارش کودکان بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
