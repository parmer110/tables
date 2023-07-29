from django.db import models
from common.models import Person, Places, CommonModel

name = "Hand Plastic Surgery"

class hand_plastic_surgery_Patient(CommonModel):
    class Meta:
        db_table = 'hand_plastic_surgery_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class HandPlasticSurgeryProcedure(CommonModel):
    # فیلدهای مربوط به روش‌های جراحی پلاستیک دست
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی پلاستیک دست')
    description = models.TextField(verbose_name='توضیحات روش جراحی پلاستیک دست')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class hand_plastic_surgery_Treatment(CommonModel):
    class Meta:
        db_table = 'hand_plastic_surgery_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(hand_plastic_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند جراحی پلاستیک دست
    hand_plastic_surgery_procedures = models.ManyToManyField(HandPlasticSurgeryProcedure, blank=True, verbose_name='روش‌های جراحی پلاستیک دست')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی پلاستیک دست بیمار {self.patient.full_name}"
