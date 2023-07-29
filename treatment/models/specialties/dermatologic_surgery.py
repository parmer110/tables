from django.db import models
from common.models import Person, Places, CommonModel

name = "Dermatologic Surgery"

class dermatologic_surgery_Patient(CommonModel):
    class Meta:
        db_table = 'dermatologic_surgery_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class DermatologicSurgeryProcedure(CommonModel):
    # فیلدهای مربوط به روش‌های جراحی پلاستیک پوست
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی پلاستیک پوست')
    description = models.TextField(verbose_name='توضیحات روش جراحی پلاستیک پوست')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class dermatologic_surgery_Treatment(CommonModel):
    class Meta:
        db_table = 'dermatologic_surgery_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(dermatologic_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند جراحی پلاستیک پوست
    dermatologic_surgery_procedures = models.ManyToManyField(DermatologicSurgeryProcedure, blank=True, verbose_name='روش‌های جراحی پلاستیک پوست')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی پلاستیک پوست بیمار {self.patient.full_name}"
