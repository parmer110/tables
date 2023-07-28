from django.db import models

name = "(Pediatric Rheumatology"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class PediatricRheumatologyProcedure(models.Model):
    # فیلدهای مربوط به روش‌های روماتولوژی کودکان
    name = models.CharField(max_length=100, verbose_name='نام روش روماتولوژی کودکان')
    description = models.TextField(verbose_name='توضیحات روش روماتولوژی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class PediatricRheumatologyTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های روماتولوژی کودکان
    name = models.CharField(max_length=100, verbose_name='نام آزمایش روماتولوژی کودکان')
    description = models.TextField(verbose_name='توضیحات آزمایش روماتولوژی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند روماتولوژی کودکان
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    pediatric_rheumatology_procedures = models.ManyToManyField(PediatricRheumatologyProcedure, blank=True, verbose_name='روش‌های روماتولوژی کودکان')
    pediatric_rheumatology_tests = models.ManyToManyField(PediatricRheumatologyTest, blank=True, verbose_name='آزمایش‌های روماتولوژی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند روماتولوژی کودکان بیمار {self.patient.full_name} در تاریخ {self.visit_date}"