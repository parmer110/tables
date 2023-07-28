from django.db import models

name = "Preventive Medicine"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class PreventiveMeasure(models.Model):
    # فیلدهای مربوط به اقدامات پزشکی پیشگیرانه
    name = models.CharField(max_length=100, verbose_name='نام اقدام پزشکی پیشگیرانه')
    description = models.TextField(verbose_name='توضیحات اقدام پزشکی پیشگیرانه')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class PreventiveTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های پزشکی پیشگیرانه
    name = models.CharField(max_length=100, verbose_name='نام آزمایش پزشکی پیشگیرانه')
    description = models.TextField(verbose_name='توضیحات آزمایش پزشکی پیشگیرانه')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند پزشکی پیشگیرانه
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    preventive_measures = models.ManyToManyField(PreventiveMeasure, blank=True, verbose_name='اقدامات پزشکی پیشگیرانه')
    preventive_tests = models.ManyToManyField(PreventiveTest, blank=True, verbose_name='آزمایش‌های پزشکی پیشگیرانه')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند پزشکی پیشگیرانه بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
