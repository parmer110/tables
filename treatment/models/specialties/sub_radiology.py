from django.db import models
from common.models import Person, Places, CommonModel

name = "Subspecialty Radiology"

# مدل بیمار
class sub_radiology_Patient(models.Model):
    class Meta:
        db_table = 'sub_radiology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

# مدل زیرتخصص پزشکی رادیولوژی (Radiology)
class Radiology(models.Model):
    patient = models.ForeignKey(sub_radiology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    imaging_type = models.CharField(max_length=100, verbose_name='نوع تصویربرداری')
    radiologist_name = models.CharField(max_length=100, verbose_name='نام رادیولوژیست')
    report = models.TextField(verbose_name='گزارش تصویربرداری')

    # فیلدهای مربوط به زیرتخصص رادیولوژی
    # ...

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"زیرتخصص پزشکی رادیولوژی برای بیمار {self.patient.full_name}"

# مدل تجویز (sub_radiology_Treatment)
class sub_radiology_Treatment(models.Model):
    class Meta:
        db_table = 'sub_radiology_Treatment'
    patient = models.ForeignKey(sub_radiology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    description = models.TextField(verbose_name='توضیحات تجویز')
    date = models.DateField(verbose_name='تاریخ تجویز')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"
