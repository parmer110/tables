from django.db import models
from common.models import Person, Places, CommonModel

name = "Surgery"

class surgery_Patient(models.Model):
    class Meta:
        db_table = 'surgery_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class SurgicalProcedure(models.Model):
    # فیلدهای مربوط به روش‌های جراحی
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی')
    description = models.TextField(verbose_name='توضیحات روش جراحی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class SurgicalComplication(models.Model):
    # فیلدهای مربوط به عوارض جراحی
    name = models.CharField(max_length=100, verbose_name='نام عارضه جراحی')
    description = models.TextField(verbose_name='توضیحات عارضه جراحی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class surgery_Treatment(models.Model):
    class Meta:
        db_table = 'surgery_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند جراحی
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    surgical_procedures = models.ManyToManyField(SurgicalProcedure, blank=True, verbose_name='روش‌های جراحی')
    surgical_complications = models.ManyToManyField(SurgicalComplication, blank=True, verbose_name='عوارض جراحی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
