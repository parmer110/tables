from django.db import models

name = "Breast Surgery"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class BreastSurgeryProcedure(models.Model):
    # فیلدهای مربوط به روش‌های جراحی سینه
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی سینه')
    description = models.TextField(verbose_name='توضیحات روش جراحی سینه')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class BreastSurgeryTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های جراحی سینه
    name = models.CharField(max_length=100, verbose_name='نام آزمایش جراحی سینه')
    description = models.TextField(verbose_name='توضیحات آزمایش جراحی سینه')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند جراحی سینه
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    breast_surgery_procedures = models.ManyToManyField(BreastSurgeryProcedure, blank=True, verbose_name='روش‌های جراحی سینه')
    breast_surgery_tests = models.ManyToManyField(BreastSurgeryTest, blank=True, verbose_name='آزمایش‌های جراحی سینه')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی سینه بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
