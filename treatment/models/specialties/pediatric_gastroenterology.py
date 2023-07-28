from django.db import models

name = "Pediatric Gastroenterology"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class PediatricGastroenterologyProcedure(models.Model):
    # فیلدهای مربوط به روش‌های گوارش کودکان
    name = models.CharField(max_length=100, verbose_name='نام روش گوارش کودکان')
    description = models.TextField(verbose_name='توضیحات روش گوارش کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class PediatricGastroenterologyTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های گوارش کودکان
    name = models.CharField(max_length=100, verbose_name='نام آزمایش گوارش کودکان')
    description = models.TextField(verbose_name='توضیحات آزمایش گوارش کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند گوارش کودکان
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    pediatric_gastroenterology_procedures = models.ManyToManyField(PediatricGastroenterologyProcedure, blank=True, verbose_name='روش‌های گوارش کودکان')
    pediatric_gastroenterology_tests = models.ManyToManyField(PediatricGastroenterologyTest, blank=True, verbose_name='آزمایش‌های گوارش کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند گوارش کودکان بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
