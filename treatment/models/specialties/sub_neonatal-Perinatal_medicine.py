from django.db import models
from common.models import Person, Places, CommonModel

name = "Subspecialty Neonatal-Perinatal Medicine"

# مدل بیمار
class sub_neonatal-Perinatal_medicine_Patient(models.Model):
    class Meta:
        db_table = 'sub_neonatal-Perinatal_medicine_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

# مدل زیرتخصص پزشکی نوزادان و نوزادان نارس (Neonatal-Perinatal Medicine)
class NeonatalPerinatalMedicine(models.Model):
    patient = models.ForeignKey(sub_neonatal-Perinatal_medicine_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    neonatal_health_issues = models.TextField(verbose_name='مشکلات بهداشتی نوزاد')
    perinatal_complications = models.TextField(verbose_name='عوارض نوزاد نارس')
    treatment_plan = models.TextField(verbose_name='طرح درمانی')
    follow_up_date = models.DateField(verbose_name='تاریخ پیگیری')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"زیرتخصص پزشکی نوزادان و نوزادان نارس برای بیمار {self.patient.full_name}"

# مدل تجویز (sub_neonatal-Perinatal_medicine_Treatment)
class sub_neonatal-Perinatal_medicine_Treatment(models.Model):
    class Meta:
        db_table = 'sub_neonatal-Perinatal_medicine_Treatment'
    patient = models.ForeignKey(sub_neonatal-Perinatal_medicine_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    description = models.TextField(verbose_name='توضیحات تجویز')
    date = models.DateField(verbose_name='تاریخ تجویز')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"
