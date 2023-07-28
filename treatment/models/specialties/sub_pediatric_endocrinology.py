from django.db import models
from common.models import Person, Places, CommonModel

name = "Subspecialty Pediatric Endocrinology"

# مدل بیمار
class sub_pediatric_endocrinology_Patient(models.Model):
    class Meta:
        db_table = 'sub_pediatric_endocrinology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

# مدل زیرتخصص پزشکی غدد کودکان (Pediatric Endocrinology)
class PediatricEndocrinology(models.Model):
    patient = models.ForeignKey(sub_pediatric_endocrinology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    endocrine_disorder = models.TextField(verbose_name='اختلال غدد')
    treatment_plan = models.TextField(verbose_name='طرح درمانی')

    # فیلدهای مربوط به زیرتخصص غدد کودکان
    # ...

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"زیرتخصص پزشکی غدد کودکان برای بیمار {self.patient.full_name}"

# مدل تجویز (sub_pediatric_endocrinology_Treatment)
class sub_pediatric_endocrinology_Treatment(models.Model):
    class Meta:
        db_table = 'sub_pediatric_endocrinology_Treatment'
    patient = models.ForeignKey(sub_pediatric_endocrinology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    description = models.TextField(verbose_name='توضیحات تجویز')
    date = models.DateField(verbose_name='تاریخ تجویز')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"
