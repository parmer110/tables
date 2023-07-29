from django.db import models
from common.models import Person, Places, CommonModel

name = "Radiation Oncology"

class radiation_oncology_Patient(CommonModel):
    class Meta:
        db_table = 'radiation_oncology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class RadiationProcedure(CommonModel):
    # فیلدهای مربوط به روش‌های پرتودرمانی و انکولوژی
    name = models.CharField(max_length=100, verbose_name='نام روش پرتودرمانی و انکولوژی')
    description = models.TextField(verbose_name='توضیحات روش پرتودرمانی و انکولوژی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class RadiationTest(CommonModel):
    # فیلدهای مربوط به آزمایش‌های پرتودرمانی و انکولوژی
    name = models.CharField(max_length=100, verbose_name='نام آزمایش پرتودرمانی و انکولوژی')
    description = models.TextField(verbose_name='توضیحات آزمایش پرتودرمانی و انکولوژی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class radiation_oncology_Treatment(CommonModel):
    class Meta:
        db_table = 'radiation_oncology_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(radiation_oncology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند پرتودرمانی و انکولوژی
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    radiation_procedures = models.ManyToManyField(RadiationProcedure, blank=True, verbose_name='روش‌های پرتودرمانی و انکولوژی')
    radiation_tests = models.ManyToManyField(RadiationTest, blank=True, verbose_name='آزمایش‌های پرتودرمانی و انکولوژی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند پرتودرمانی و انکولوژی بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
