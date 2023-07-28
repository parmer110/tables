from django.db import models

name = "Thoracic Surgery"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class ThoracicSurgeryProcedure(models.Model):
    # فیلدهای مربوط به روش‌های جراحی قفسه سینه
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی قفسه سینه')
    description = models.TextField(verbose_name='توضیحات روش جراحی قفسه سینه')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class ThoracicSurgeryTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های جراحی قفسه سینه
    name = models.CharField(max_length=100, verbose_name='نام آزمایش جراحی قفسه سینه')
    description = models.TextField(verbose_name='توضیحات آزمایش جراحی قفسه سینه')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند جراحی قفسه سینه
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    thoracic_surgery_procedures = models.ManyToManyField(ThoracicSurgeryProcedure, blank=True, verbose_name='روش‌های جراحی قفسه سینه')
    thoracic_surgery_tests = models.ManyToManyField(ThoracicSurgeryTest, blank=True, verbose_name='آزمایش‌های جراحی قفسه سینه')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی قفسه سینه بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
