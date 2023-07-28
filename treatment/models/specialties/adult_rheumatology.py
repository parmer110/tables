from django.db import models

name= "Adult Rheumatology"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class AdultRheumatologyProcedure(models.Model):
    # فیلدهای مربوط به روش‌های روماتولوژی بالغین
    name = models.CharField(max_length=100, verbose_name='نام روش روماتولوژی بالغین')
    description = models.TextField(verbose_name='توضیحات روش روماتولوژی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class AdultRheumatologyTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های روماتولوژی بالغین
    name = models.CharField(max_length=100, verbose_name='نام آزمایش روماتولوژی بالغین')
    description = models.TextField(verbose_name='توضیحات آزمایش روماتولوژی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند روماتولوژی بالغین
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    adult_rheumatology_procedures = models.ManyToManyField(AdultRheumatologyProcedure, blank=True, verbose_name='روش‌های روماتولوژی بالغین')
    adult_rheumatology_tests = models.ManyToManyField(AdultRheumatologyTest, blank=True, verbose_name='آزمایش‌های روماتولوژی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند روماتولوژی بالغین بیمار {self.patient.full_name} در تاریخ {self.visit_date}"