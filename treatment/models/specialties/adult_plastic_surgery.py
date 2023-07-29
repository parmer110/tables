from django.db import models
from common.models import Person, Places, CommonModel

name = "Adult Plastic Surgery"

class adult_plastic_surgery_Patient(CommonModel):
    class Meta:
        db_table = 'adult_plastic_surgery_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class AdultPlasticSurgeryProcedure(CommonModel):
    # فیلدهای مربوط به روش‌های جراحی پلاستیک بالغین
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی پلاستیک بالغین')
    description = models.TextField(verbose_name='توضیحات روش جراحی پلاستیک بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class AdultPlasticSurgeryTest(CommonModel):
    # فیلدهای مربوط به آزمایش‌های جراحی پلاستیک بالغین
    name = models.CharField(max_length=100, verbose_name='نام آزمایش جراحی پلاستیک بالغین')
    description = models.TextField(verbose_name='توضیحات آزمایش جراحی پلاستیک بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class adult_plastic_surgery_Treatment(CommonModel):
    class Meta:
        db_table = 'adult_plastic_surgery_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(adult_plastic_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند جراحی پلاستیک بالغین
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    adult_plastic_surgery_procedures = models.ManyToManyField(AdultPlasticSurgeryProcedure, blank=True, verbose_name='روش‌های جراحی پلاستیک بالغین')
    adult_plastic_surgery_tests = models.ManyToManyField(AdultPlasticSurgeryTest, blank=True, verbose_name='آزمایش‌های جراحی پلاستیک بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی پلاستیک بالغین بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
