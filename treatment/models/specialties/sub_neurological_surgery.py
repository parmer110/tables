from django.db import models
from common.models import Person, Places, CommonModel

name = "Subspecialty Neurological Surgery"

# مدل بیمار
class sub_neurological_surgery_Patient(CommonModel):
    class Meta:
        db_table = 'sub_neurological_surgery_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

# مدل زیرتخصص پزشکی جراحی مغز و اعصاب (Neurological Surgery)
class NeurologicalSurgery(CommonModel):
    patient = models.ForeignKey(sub_neurological_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    brain_condition = models.TextField(verbose_name='وضعیت مغز')
    neurological_issues = models.TextField(verbose_name='مشکلات عصبی')
    surgical_approach = models.TextField(verbose_name='روش جراحی')
    postoperative_care = models.TextField(verbose_name='مراقبت پس از جراحی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"زیرتخصص پزشکی جراحی مغز و اعصاب برای بیمار {self.patient.full_name}"

# مدل تجویز (sub_neurological_surgery_Treatment)
class sub_neurological_surgery_Treatment(CommonModel):
    class Meta:
        db_table = 'sub_neurological_surgery_Treatment'
    patient = models.ForeignKey(sub_neurological_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    description = models.TextField(verbose_name='توضیحات تجویز')
    date = models.DateField(verbose_name='تاریخ تجویز')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"
