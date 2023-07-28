from django.db import models

name = "Pediatric Endocrinology"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class PediatricEndocrinologyProcedure(models.Model):
    # فیلدهای مربوط به روش‌های غدد کودکان
    name = models.CharField(max_length=100, verbose_name='نام روش غدد کودکان')
    description = models.TextField(verbose_name='توضیحات روش غدد کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class PediatricEndocrinologyTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های غدد کودکان
    name = models.CharField(max_length=100, verbose_name='نام آزمایش غدد کودکان')
    description = models.TextField(verbose_name='توضیحات آزمایش غدد کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند غدد کودکان
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    pediatric_endocrinology_procedures = models.ManyToManyField(PediatricEndocrinologyProcedure, blank=True, verbose_name='روش‌های غدد کودکان')
    pediatric_endocrinology_tests = models.ManyToManyField(PediatricEndocrinologyTest, blank=True, verbose_name='آزمایش‌های غدد کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند غدد کودکان بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
