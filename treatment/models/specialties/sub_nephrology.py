from django.db import models
from common.models import Person, Places, CommonModel

name = "Subspecialty Nephrology"

# مدل بیمار
class sub_nephrology_Patient(CommonModel):
    class Meta:
        db_table = 'sub_nephrology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

# مدل زیرتخصص پزشکی نفرولوژی (Nephrology)
class Nephrology(CommonModel):
    patient = models.ForeignKey(sub_nephrology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    kidney_condition = models.TextField(verbose_name='وضعیت کلیه')
    urinary_issues = models.TextField(verbose_name='مشکلات ادراری')
    treatment_plan = models.TextField(verbose_name='طرح درمانی')
    follow_up_date = models.DateField(verbose_name='تاریخ پیگیری')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"زیرتخصص پزشکی نفرولوژی برای بیمار {self.patient.full_name}"

# مدل تجویز (sub_nephrology_Treatment)
class sub_nephrology_Treatment(CommonModel):
    class Meta:
        db_table = 'sub_nephrology_Treatment'
    patient = models.ForeignKey(sub_nephrology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    description = models.TextField(verbose_name='توضیحات تجویز')
    date = models.DateField(verbose_name='تاریخ تجویز')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"
