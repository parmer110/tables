from django.db import models
from common.models import Person, Places, CommonModel

name = "Oncologic Plastic Surgery"

# مدل بیمار
class oncologic_plastic_surgery_Patient(CommonModel):
    class Meta:
        db_table = 'oncologic_plastic_surgery_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

# مدل تخصص جراحی پلاستیک سرطان (Oncologic Plastic Surgery)
class OncologicPlasticSurgery(CommonModel):
    patient = models.ForeignKey(oncologic_plastic_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    type_of_cancer = models.CharField(max_length=100, verbose_name='نوع سرطان')
    surgical_approach = models.TextField(verbose_name='روش جراحی')
    reconstruction_technique = models.TextField(verbose_name='تکنیک بازسازی')
    success_rate = models.FloatField(verbose_name='نرخ موفقیت در جراحی')
    postoperative_recovery = models.TextField(verbose_name='بازیابی پس از جراحی')
    complications = models.TextField(verbose_name='ممکن است طی جراحی پیش آید')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"جراحی پلاستیک سرطان برای بیمار {self.patient.full_name}"

# مدل تجویز (oncologic_plastic_surgery_Treatment)
class oncologic_plastic_surgery_Treatment(CommonModel):
    class Meta:
        db_table = 'oncologic_plastic_surgery_Treatment'
    patient = models.ForeignKey(oncologic_plastic_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    description = models.TextField(verbose_name='توضیحات تجویز')
    date = models.DateField(verbose_name='تاریخ تجویز')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"



