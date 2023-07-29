from django.db import models
from common.models import Person, Places, CommonModel

name = "Subspecialty Adult Cardiology"

# مدل بیمار
class sub_adult_cardiology_Patient(CommonModel):
    class Meta:
        db_table = 'sub_adult_cardiology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

# مدل زیرتخصص پزشکی قلب و عروق بالغین (Adult Cardiology)
class AdultCardiology(CommonModel):
    patient = models.ForeignKey(sub_adult_cardiology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    cardiac_diagnosis = models.TextField(verbose_name='تشخیص قلبی')
    treatment_plan = models.TextField(verbose_name='طرح درمانی')
    medication_list = models.TextField(verbose_name='لیست داروها')
    follow_up_date = models.DateField(verbose_name='تاریخ پیگیری')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"زیرتخصص پزشکی قلب و عروق بالغین برای بیمار {self.patient.full_name}"

# مدل تجویز (sub_adult_cardiology_Treatment)
class sub_adult_cardiology_Treatment(CommonModel):
    class Meta:
        db_table = 'sub_adult_cardiology_Treatment'
    patient = models.ForeignKey(sub_adult_cardiology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    description = models.TextField(verbose_name='توضیحات تجویز')
    date = models.DateField(verbose_name='تاریخ تجویز')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"
