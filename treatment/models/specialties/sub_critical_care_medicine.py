from django.db import models
from common.models import Person, Places, CommonModel

name = "Subspecialty Critical Care Medicine"

# مدل بیمار
class sub_critical_care_medicine_Patient(CommonModel):
    class Meta:
        db_table = 'sub_critical_care_medicine_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

# مدل تخصص مراقبت‌های وخیم (Critical Care Medicine)
class CriticalCareMedicine(CommonModel):
    patient = models.ForeignKey(sub_critical_care_medicine_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    condition = models.CharField(max_length=100, verbose_name='وضعیت بیماری')
    treatment_plan = models.TextField(verbose_name='طرح درمانی')
    medications = models.TextField(verbose_name='داروها')
    medical_equipment = models.TextField(verbose_name='تجهیزات پزشکی')
    monitoring_parameters = models.TextField(verbose_name='پارامترهای نظارتی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"مراقبت‌های وخیم برای بیمار {self.patient.full_name}"

# مدل تجویز (sub_critical_care_medicine_Treatment)
class sub_critical_care_medicine_Treatment(CommonModel):
    class Meta:
        db_table = 'sub_critical_care_medicine_Treatment'
    patient = models.ForeignKey(sub_critical_care_medicine_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    description = models.TextField(verbose_name='توضیحات تجویز')
    date = models.DateField(verbose_name='تاریخ تجویز')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"
