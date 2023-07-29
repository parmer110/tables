from django.db import models
from common.models import Person, Places, CommonModel

name = "Subspecialty Pediatric Cardiology"

# مدل بیمار
class sub_pediatric_cardiology_Patient(CommonModel):
    class Meta:
        db_table = 'sub_pediatric_cardiology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

# مدل زیرتخصص پزشکی قلب و عروق کودکان (Pediatric Cardiology)
class PediatricCardiology(CommonModel):
    patient = models.ForeignKey(sub_pediatric_cardiology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    congenital_heart_disease = models.TextField(verbose_name='بیماری‌های قلبی خلقی')
    diagnostic_tests = models.TextField(verbose_name='آزمایشات تشخیصی')
    treatment_plan = models.TextField(verbose_name='طرح درمانی')
    follow_up_date = models.DateField(verbose_name='تاریخ پیگیری')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"زیرتخصص پزشکی قلب و عروق کودکان برای بیمار {self.patient.full_name}"

# مدل تجویز (sub_pediatric_cardiology_Treatment)
class sub_pediatric_cardiology_Treatment(CommonModel):
    class Meta:
        db_table = 'sub_pediatric_cardiology_Treatment'
    patient = models.ForeignKey(sub_pediatric_cardiology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    description = models.TextField(verbose_name='توضیحات تجویز')
    date = models.DateField(verbose_name='تاریخ تجویز')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"
