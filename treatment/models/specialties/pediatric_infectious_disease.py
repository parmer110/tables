from django.db import models
from common.models import Person, Places, CommonModel

name = "Pediatric Infectious Disease"

class pediatric_infectious_disease_Patient(CommonModel):
    class Meta:
        db_table = 'pediatric_infectious_disease_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class PediatricInfectiousDiseaseProcedure(CommonModel):
    # فیلدهای مربوط به روش‌های عفونی کودکان
    name = models.CharField(max_length=100, verbose_name='نام روش عفونی کودکان')
    description = models.TextField(verbose_name='توضیحات روش عفونی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class PediatricInfectiousDiseaseTest(CommonModel):
    # فیلدهای مربوط به آزمایش‌های عفونی کودکان
    name = models.CharField(max_length=100, verbose_name='نام آزمایش عفونی کودکان')
    description = models.TextField(verbose_name='توضیحات آزمایش عفونی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class pediatric_infectious_disease_Treatment(CommonModel):
    class Meta:
        db_table = 'pediatric_infectious_disease_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(pediatric_infectious_disease_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند عفونی کودکان
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    pediatric_infectious_disease_procedures = models.ManyToManyField(PediatricInfectiousDiseaseProcedure, blank=True, verbose_name='روش‌های عفونی کودکان')
    pediatric_infectious_disease_tests = models.ManyToManyField(PediatricInfectiousDiseaseTest, blank=True, verbose_name='آزمایش‌های عفونی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند عفونی کودکان بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
