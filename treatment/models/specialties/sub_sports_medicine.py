from django.db import models
from common.models import Person, Places, CommonModel

name = "Subspecialty Sports Medicine"

# مدل بیمار
class sub_sports_medicine_Patient(CommonModel):
    class Meta:
        db_table = 'sub_sports_medicine_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

# مدل زیرتخصص پزشکی ورزشی (Sports Medicine)
class SportsMedicine(CommonModel):
    patient = models.ForeignKey(sub_sports_medicine_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    sports_injuries = models.TextField(verbose_name='صدمات ورزشی')
    physical_examinations = models.TextField(verbose_name='بررسی‌های فیزیکی')
    treatment_options = models.TextField(verbose_name='گزینه‌های درمانی')

    # فیلدهای مربوط به زیرتخصص پزشکی ورزشی
    # ...

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"زیرتخصص پزشکی ورزشی برای بیمار {self.patient.full_name}"

# مدل تجویز (sub_sports_medicine_Treatment)
class sub_sports_medicine_Treatment(CommonModel):
    class Meta:
        db_table = 'sub_sports_medicine_Treatment'
    patient = models.ForeignKey(sub_sports_medicine_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    description = models.TextField(verbose_name='توضیحات تجویز')
    date = models.DateField(verbose_name='تاریخ تجویز')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"

