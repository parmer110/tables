from django.db import models

name = "Adult Pulmonology"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class AdultPulmonologyProcedure(models.Model):
    # فیلدهای مربوط به روش‌های ریه بالغین
    name = models.CharField(max_length=100, verbose_name='نام روش ریه بالغین')
    description = models.TextField(verbose_name='توضیحات روش ریه بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class AdultPulmonologyTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های ریه بالغین
    name = models.CharField(max_length=100, verbose_name='نام آزمایش ریه بالغین')
    description = models.TextField(verbose_name='توضیحات آزمایش ریه بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند ریه بالغین
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    adult_pulmonology_procedures = models.ManyToManyField(AdultPulmonologyProcedure, blank=True, verbose_name='روش‌های ریه بالغین')
    adult_pulmonology_tests = models.ManyToManyField(AdultPulmonologyTest, blank=True, verbose_name='آزمایش‌های ریه بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند ریه بالغین بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
