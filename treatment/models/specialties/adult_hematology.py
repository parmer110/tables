from django.db import models

name = "Adult Hematology"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class AdultHematologyProcedure(models.Model):
    # فیلدهای مربوط به روش‌های هماتولوژی بالغین
    name = models.CharField(max_length=100, verbose_name='نام روش هماتولوژی بالغین')
    description = models.TextField(verbose_name='توضیحات روش هماتولوژی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class AdultHematologyTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های هماتولوژی بالغین
    name = models.CharField(max_length=100, verbose_name='نام آزمایش هماتولوژی بالغین')
    description = models.TextField(verbose_name='توضیحات آزمایش هماتولوژی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند هماتولوژی بالغین
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    adult_hematology_procedures = models.ManyToManyField(AdultHematologyProcedure, blank=True, verbose_name='روش‌های هماتولوژی بالغین')
    adult_hematology_tests = models.ManyToManyField(AdultHematologyTest, blank=True, verbose_name='آزمایش‌های هماتولوژی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند هماتولوژی بالغین بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
