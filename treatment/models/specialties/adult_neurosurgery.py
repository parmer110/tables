from django.db import models

name = "Adult Neurosurgery"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class AdultNeurosurgeryProcedure(models.Model):
    # فیلدهای مربوط به روش‌های جراحی مغز و اعصاب بالغین
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی مغز و اعصاب بالغین')
    description = models.TextField(verbose_name='توضیحات روش جراحی مغز و اعصاب بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class AdultNeurosurgeryTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های جراحی مغز و اعصاب بالغین
    name = models.CharField(max_length=100, verbose_name='نام آزمایش جراحی مغز و اعصاب بالغین')
    description = models.TextField(verbose_name='توضیحات آزمایش جراحی مغز و اعصاب بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند جراحی مغز و اعصاب بالغین
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    adult_neurosurgery_procedures = models.ManyToManyField(AdultNeurosurgeryProcedure, blank=True, verbose_name='روش‌های جراحی مغز و اعصاب بالغین')
    adult_neurosurgery_tests = models.ManyToManyField(AdultNeurosurgeryTest, blank=True, verbose_name='آزمایش‌های جراحی مغز و اعصاب بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی مغز و اعصاب بالغین بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
