from django.db import models

name = "Adult Infectious Disease"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class AdultInfectiousDiseaseProcedure(models.Model):
    # فیلدهای مربوط به روش‌های عفونی بالغین
    name = models.CharField(max_length=100, verbose_name='نام روش عفونی بالغین')
    description = models.TextField(verbose_name='توضیحات روش عفونی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class AdultInfectiousDiseaseTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های عفونی بالغین
    name = models.CharField(max_length=100, verbose_name='نام آزمایش عفونی بالغین')
    description = models.TextField(verbose_name='توضیحات آزمایش عفونی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند عفونی بالغین
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    adult_infectious_disease_procedures = models.ManyToManyField(AdultInfectiousDiseaseProcedure, blank=True, verbose_name='روش‌های عفونی بالغین')
    adult_infectious_disease_tests = models.ManyToManyField(AdultInfectiousDiseaseTest, blank=True, verbose_name='آزمایش‌های عفونی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند عفونی بالغین بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
