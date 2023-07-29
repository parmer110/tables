from django.db import models
from common.models import Person, Places, CommonModel

name = "Subspecialty Rheumatology"

# مدل بیمار
class sub_rheumatology_Patient(CommonModel):
    class Meta:
        db_table = 'sub_rheumatology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

# مدل زیرتخصص پزشکی روماتولوژی (Rheumatology)
class Rheumatology(CommonModel):
    patient = models.ForeignKey(sub_rheumatology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    rheumatic_conditions = models.TextField(verbose_name='شرایط روماتولوژیک')
    diagnostic_tests = models.TextField(verbose_name='آزمایش‌های تشخیصی')
    treatment_options = models.TextField(verbose_name='گزینه‌های درمانی')

    # فیلدهای مربوط به زیرتخصص روماتولوژی
    # ...

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"زیرتخصص پزشکی روماتولوژی برای بیمار {self.patient.full_name}"

# مدل تجویز (sub_rheumatology_Treatment)
class sub_rheumatology_Treatment(CommonModel):
    class Meta:
        db_table = 'sub_rheumatology_Treatment'
    patient = models.ForeignKey(sub_rheumatology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    description = models.TextField(verbose_name='توضیحات تجویز')
    date = models.DateField(verbose_name='تاریخ تجویز')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"
