from django.db import models
from common.models import Person, Places, CommonModel

name = "Anesthesiology"

class dermatology_Patient(models.Model):
    class Meta:
        db_table = 'dermatology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class SkinCondition(models.Model):
    # فیلدهای مربوط به بیماری‌های پوستی
    name = models.CharField(max_length=100, verbose_name='نام بیماری')
    description = models.TextField(verbose_name='توضیحات بیماری')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Prescription(models.Model):
    # فیلدهای مربوط به نسخه داروها
    medication = models.CharField(max_length=100, verbose_name='نام دارو')
    dosage = models.CharField(max_length=50, verbose_name='مقدار دوز دارو')
    usage_instructions = models.TextField(verbose_name='دستورات مصرف دارو')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.medication

class dermatology_Treatment(models.Model):
    class Meta:
        db_table = 'dermatology_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(dermatology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند درمانی
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    diagnosis = models.TextField(verbose_name='تشخیص بیماری')
    skin_conditions = models.ManyToManyField(SkinCondition, blank=True, verbose_name='بیماری‌های پوستی')
    prescriptions = models.ManyToManyField(Prescription, blank=True, verbose_name='نسخه‌های دارویی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند درمانی بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
