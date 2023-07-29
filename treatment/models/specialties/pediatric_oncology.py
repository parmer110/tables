from django.db import models
from common.models import Person, Places, CommonModel

name = "Pediatric Oncology"

class pediatric_oncology_Patient(CommonModel):
    class Meta:
        db_table = 'pediatric_oncology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class PediatricOncologyProcedure(CommonModel):
    # فیلدهای مربوط به روش‌های جراحی آنکولوژی کودکان
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی آنکولوژی کودکان')
    description = models.TextField(verbose_name='توضیحات روش جراحی آنکولوژی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class PediatricOncologyTest(CommonModel):
    # فیلدهای مربوط به آزمایش‌های آنکولوژی کودکان
    name = models.CharField(max_length=100, verbose_name='نام آزمایش آنکولوژی کودکان')
    description = models.TextField(verbose_name='توضیحات آزمایش آنکولوژی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class pediatric_oncology_Treatment(CommonModel):
    class Meta:
        db_table = 'pediatric_oncology_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(pediatric_oncology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند آنکولوژی کودکان
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    pediatric_oncology_procedures = models.ManyToManyField(PediatricOncologyProcedure, blank=True, verbose_name='روش‌های جراحی آنکولوژی کودکان')
    pediatric_oncology_tests = models.ManyToManyField(PediatricOncologyTest, blank=True, verbose_name='آزمایش‌های آنکولوژی کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند آنکولوژی کودکان بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
