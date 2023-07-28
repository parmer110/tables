from django.db import models
from common.models import Person, Places, CommonModel

name = "Hand Surgery"

class hand_surgery_Patient(models.Model):
    class Meta:
        db_table = 'hand_surgery_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class HandSurgeryProcedure(models.Model):
    # فیلدهای مربوط به روش‌های جراحی دست
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی دست')
    description = models.TextField(verbose_name='توضیحات روش جراحی دست')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class HandSurgeryTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های جراحی دست
    name = models.CharField(max_length=100, verbose_name='نام آزمایش جراحی دست')
    description = models.TextField(verbose_name='توضیحات آزمایش جراحی دست')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class hand_surgery_Treatment(models.Model):
    class Meta:
        db_table = 'hand_surgery_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(hand_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند جراحی دست
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    hand_surgery_procedures = models.ManyToManyField(HandSurgeryProcedure, blank=True, verbose_name='روش‌های جراحی دست')
    hand_surgery_tests = models.ManyToManyField(HandSurgeryTest, blank=True, verbose_name='آزمایش‌های جراحی دست')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی دست بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
