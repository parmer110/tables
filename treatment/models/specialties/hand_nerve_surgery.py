from django.db import models

name = "Hand Nerve Surgery"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class HandNerveSurgeryProcedure(models.Model):
    # فیلدهای مربوط به روش‌های جراحی اعصاب دست
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی اعصاب دست')
    description = models.TextField(verbose_name='توضیحات روش جراحی اعصاب دست')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class HandNerveSurgeryTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های جراحی اعصاب دست
    name = models.CharField(max_length=100, verbose_name='نام آزمایش جراحی اعصاب دست')
    description = models.TextField(verbose_name='توضیحات آزمایش جراحی اعصاب دست')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند جراحی اعصاب دست
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    hand_nerve_surgery_procedures = models.ManyToManyField(HandNerveSurgeryProcedure, blank=True, verbose_name='روش‌های جراحی اعصاب دست')
    hand_nerve_surgery_tests = models.ManyToManyField(HandNerveSurgeryTest, blank=True, verbose_name='آزمایش‌های جراحی اعصاب دست')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی اعصاب دست بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
