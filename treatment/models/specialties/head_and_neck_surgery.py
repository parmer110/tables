from django.db import models

name = "Head and Neck Surgery"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class HeadAndNeckSurgeryProcedure(models.Model):
    # فیلدهای مربوط به روش‌های جراحی سر و گردن
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی سر و گردن')
    description = models.TextField(verbose_name='توضیحات روش جراحی سر و گردن')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class HeadAndNeckSurgeryTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های جراحی سر و گردن
    name = models.CharField(max_length=100, verbose_name='نام آزمایش جراحی سر و گردن')
    description = models.TextField(verbose_name='توضیحات آزمایش جراحی سر و گردن')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند جراحی سر و گردن
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    head_and_neck_surgery_procedures = models.ManyToManyField(HeadAndNeckSurgeryProcedure, blank=True, verbose_name='روش‌های جراحی سر و گردن')
    head_and_neck_surgery_tests = models.ManyToManyField(HeadAndNeckSurgeryTest, blank=True, verbose_name='آزمایش‌های جراحی سر و گردن')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی سر و گردن بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
