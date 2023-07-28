from django.db import models

name="Diagnostic Radiology"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class ImagingModality(models.Model):
    # فیلدهای مربوط به انواع تصویربرداری پزشکی
    name = models.CharField(max_length=100, verbose_name='نوع تصویربرداری')
    description = models.TextField(verbose_name='توضیحات تصویربرداری')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class RadiologyFinding(models.Model):
    # فیلدهای مربوط به یافته‌های رادیولوژی
    name = models.CharField(max_length=100, verbose_name='نام یافته')
    description = models.TextField(verbose_name='توضیحات یافته')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند رادیولوژی تشخیصی
    imaging_modality = models.ForeignKey(ImagingModality, on_delete=models.PROTECT, verbose_name='نوع تصویربرداری')
    imaging_date = models.DateTimeField(verbose_name='تاریخ تصویربرداری')
    radiology_findings = models.ManyToManyField(RadiologyFinding, blank=True, verbose_name='یافته‌های رادیولوژی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند رادیولوژی تشخیصی بیمار {self.patient.full_name} در تاریخ {self.imaging_date}"
