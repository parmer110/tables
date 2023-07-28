from django.db import models
from common.models import Person, Places, CommonModel

name = "Urology"

class urology_Patient(models.Model):
    class Meta:
        db_table = 'urology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class UrologicalProcedure(models.Model):
    # فیلدهای مربوط به روش‌های اورولوژی
    name = models.CharField(max_length=100, verbose_name='نام روش اورولوژی')
    description = models.TextField(verbose_name='توضیحات روش اورولوژی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class UrologicalTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های اورولوژی
    name = models.CharField(max_length=100, verbose_name='نام آزمایش اورولوژی')
    description = models.TextField(verbose_name='توضیحات آزمایش اورولوژی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class urology_Treatment(models.Model):
    class Meta:
        db_table = 'urology_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(urology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند اورولوژی
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    urological_procedures = models.ManyToManyField(UrologicalProcedure, blank=True, verbose_name='روش‌های اورولوژی')
    urological_tests = models.ManyToManyField(UrologicalTest, blank=True, verbose_name='آزمایش‌های اورولوژی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند اورولوژی بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
