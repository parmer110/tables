from django.db import models
from common.models import Person, Places, CommonModel

name="Diagnostic Radiology"

class diagnostic_radiology_Patient(CommonModel):
    class Meta:
        db_table = 'diagnostic_radiology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class ImagingModality(CommonModel):
    # فیلدهای مربوط به انواع تصویربرداری پزشکی
    name = models.CharField(max_length=100, verbose_name='نوع تصویربرداری')
    description = models.TextField(verbose_name='توضیحات تصویربرداری')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class RadiologyFinding(CommonModel):
    # فیلدهای مربوط به یافته‌های رادیولوژی
    name = models.CharField(max_length=100, verbose_name='نام یافته')
    description = models.TextField(verbose_name='توضیحات یافته')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class diagnostic_radiology_Treatment(CommonModel):
    class Meta:
        db_table = 'diagnostic_radiology_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(diagnostic_radiology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند رادیولوژی تشخیصی
    imaging_modality = models.ForeignKey(ImagingModality, on_delete=models.PROTECT, verbose_name='نوع تصویربرداری')
    imaging_date = models.DateTimeField(verbose_name='تاریخ تصویربرداری')
    radiology_findings = models.ManyToManyField(RadiologyFinding, blank=True, verbose_name='یافته‌های رادیولوژی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند رادیولوژی تشخیصی بیمار {self.patient.full_name} در تاریخ {self.imaging_date}"
