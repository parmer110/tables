from django.db import models
from common.models import Person, Places, CommonModel

name = "Subspecialty Pediatric Hematology-Oncology"

# مدل بیمار
class sub_pediatric_hematology-oncology_Patient(models.Model):
    class Meta:
        db_table = 'sub_pediatric_hematology-oncology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

# مدل زیرتخصص پزشکی هماتولوژی و آنکولوژی کودکان (Pediatric Hematology-Oncology)
class PediatricHematologyOncology(models.Model):
    patient = models.ForeignKey(sub_pediatric_hematology-oncology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    type_of_cancer = models.CharField(max_length=100, verbose_name='نوع سرطان')
    blood_disorder = models.TextField(verbose_name='اختلال خونی')
    treatment_plan = models.TextField(verbose_name='طرح درمانی')

    # فیلدهای مربوط به زیرتخصص هماتولوژی و آنکولوژی کودکان
    # ...

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"زیرتخصص پزشکی هماتولوژی و آنکولوژی کودکان برای بیمار {self.patient.full_name}"

# مدل تجویز (sub_pediatric_hematology-oncology_Treatment)
class sub_pediatric_hematology-oncology_Treatment(models.Model):
    class Meta:
        db_table = 'sub_pediatric_hematology-oncology_Treatment'
    patient = models.ForeignKey(sub_pediatric_hematology-oncology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    description = models.TextField(verbose_name='توضیحات تجویز')
    date = models.DateField(verbose_name='تاریخ تجویز')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"
