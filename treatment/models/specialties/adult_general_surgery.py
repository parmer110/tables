from django.db import models

name = "Adult General Surgery"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class AdultGeneralSurgeryProcedure(models.Model):
    # فیلدهای مربوط به روش‌های جراحی عمومی بالغین
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی عمومی بالغین')
    description = models.TextField(verbose_name='توضیحات روش جراحی عمومی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class AdultGeneralSurgeryTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های جراحی عمومی بالغین
    name = models.CharField(max_length=100, verbose_name='نام آزمایش جراحی عمومی بالغین')
    description = models.TextField(verbose_name='توضیحات آزمایش جراحی عمومی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند جراحی عمومی بالغین
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    adult_general_surgery_procedures = models.ManyToManyField(AdultGeneralSurgeryProcedure, blank=True, verbose_name='روش‌های جراحی عمومی بالغین')
    adult_general_surgery_tests = models.ManyToManyField(AdultGeneralSurgeryTest, blank=True, verbose_name='آزمایش‌های جراحی عمومی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی عمومی بالغین بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
