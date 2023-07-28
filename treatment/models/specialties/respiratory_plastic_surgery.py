from django.db import models
from common.models import Person, Places, CommonModel

name = "Respiratory Plastic Surgery"

class respiratory_plastic_surgery_Patient(models.Model):
    class Meta:
        db_table = 'respiratory_plastic_surgery_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن بیمار')
    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class RespiratorySurgeryProcedure(models.Model):
    # فیلدهای مربوط به روش‌های جراحی تنفسی
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی تنفسی')
    description = models.TextField(verbose_name='توضیحات روش جراحی تنفسی')
    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class RespiratorySurgeryHistory(models.Model):
    # بیمار مربوط به تاریخچه‌ی جراحی تنفسی
    patient = models.ForeignKey(respiratory_plastic_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # روش‌های جراحی تنفسی انجام شده برای بیمار
    respiratory_surgery_procedures = models.ManyToManyField(RespiratorySurgeryProcedure, blank=True, verbose_name='روش‌های جراحی تنفسی')

    # تاریخ جراحی تنفسی
    surgery_date = models.DateField(verbose_name='تاریخ جراحی تنفسی')

    # توضیحات دیگر مرتبط با تاریخچه‌ی جراحی تنفسی
    description = models.TextField(verbose_name='توضیحات تاریخچه‌ی جراحی تنفسی')
    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تاریخچه‌ی جراحی تنفسی بیمار {self.patient.full_name}"

class respiratory_plastic_surgery_Treatment(models.Model):
    class Meta:
        db_table = 'respiratory_plastic_surgery_Treatment'
    # بیمار مربوط به درمان
    patient = models.ForeignKey(respiratory_plastic_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # نام درمان
    name = models.CharField(max_length=100, verbose_name='نام درمان')

    # تاریخ شروع درمان
    start_date = models.DateField(verbose_name='تاریخ شروع درمان')

    # توضیحات درمان
    description = models.TextField(verbose_name='توضیحات درمان')
    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"درمان {self.name} برای بیمار {self.patient.full_name}"
