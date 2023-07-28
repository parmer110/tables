from django.db import models
from common.models import Person, Places, CommonModel

name = "Subspecialty Neurology"

# مدل بیمار
class sub_neurology_Patient(models.Model):
    class Meta:
        db_table = 'sub_neurology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

# مدل زیرتخصص پزشکی عصب‌شناسی (Neurology)
class Neurology(models.Model):
    patient = models.ForeignKey(sub_neurology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    neurologic_conditions = models.TextField(verbose_name='بیماری‌ها و مشکلات عصبی')
    diagnostic_tests = models.TextField(verbose_name='آزمایشات تشخیصی')
    treatment_options = models.TextField(verbose_name='گزینه‌های درمانی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"زیرتخصص پزشکی عصب‌شناسی برای بیمار {self.patient.full_name}"

# مدل تجویز (sub_neurology_Treatment)
class sub_neurology_Treatment(models.Model):
    class Meta:
        db_table = 'sub_neurology_Treatment'
    patient = models.ForeignKey(sub_neurology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    description = models.TextField(verbose_name='توضیحات تجویز')
    date = models.DateField(verbose_name='تاریخ تجویز')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"
