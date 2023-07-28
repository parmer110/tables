from django.db import models
from common.models import Person, Places, CommonModel

name = "Reconstructive Plastic Surgery"

class reconstructive_plastic_surgery_Patient(models.Model):
    class Meta:
        db_table = 'reconstructive_plastic_surgery_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class ReconstructivePlasticSurgeryProcedure(models.Model):
    # فیلدهای مربوط به روش‌های جراحی پلاستیک ترمیمی
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی پلاستیک ترمیمی')
    description = models.TextField(verbose_name='توضیحات روش جراحی پلاستیک ترمیمی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class reconstructive_plastic_surgery_Treatment(models.Model):
    class Meta:
        db_table = 'reconstructive_plastic_surgery_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(reconstructive_plastic_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند جراحی پلاستیک ترمیمی
    reconstructive_plastic_surgery_procedures = models.ManyToManyField(ReconstructivePlasticSurgeryProcedure, blank=True, verbose_name='روش‌های جراحی پلاستیک ترمیمی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی پلاستیک ترمیمی بیمار {self.patient.full_name}"
