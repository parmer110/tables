from django.db import models
from common.models import Person, Places, CommonModel

name = "Pediatric Cardiovascular Surgery"

class pediatric_cardiovascular_surgery_Patient(CommonModel):
    class Meta:
        db_table = 'pediatric_cardiovascular_surgery_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class PediatricCardiovascularSurgeryProcedure(CommonModel):
    # فیلدهای مربوط به روش‌های جراحی قلب و عروق کودکان
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی قلب و عروق کودکان')
    description = models.TextField(verbose_name='توضیحات روش جراحی قلب و عروق کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class PediatricCardiovascularSurgeryTest(CommonModel):
    # فیلدهای مربوط به آزمایش‌های جراحی قلب و عروق کودکان
    name = models.CharField(max_length=100, verbose_name='نام آزمایش جراحی قلب و عروق کودکان')
    description = models.TextField(verbose_name='توضیحات آزمایش جراحی قلب و عروق کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class pediatric_cardiovascular_surgery_Treatment(CommonModel):
    class Meta:
        db_table = 'pediatric_cardiovascular_surgery_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(pediatric_cardiovascular_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند جراحی قلب و عروق کودکان
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    pediatric_cardiovascular_surgery_procedures = models.ManyToManyField(PediatricCardiovascularSurgeryProcedure, blank=True, verbose_name='روش‌های جراحی قلب و عروق کودکان')
    pediatric_cardiovascular_surgery_tests = models.ManyToManyField(PediatricCardiovascularSurgeryTest, blank=True, verbose_name='آزمایش‌های جراحی قلب و عروق کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی قلب و عروق کودکان بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
