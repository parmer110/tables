from django.db import models
from common.models import Person, Places, CommonModel

name = "Breast Craniofacial Surgery"

# مدل بیمار
class breast_craniofacial_surgery_Patient(models.Model):
    class Meta:
        db_table = 'breast_craniofacial_surgery_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

# مدل تخصص جراحی پلاستیک صورت سینه (Breast Craniofacial Surgery)
class BreastCraniofacialSurgery(models.Model):
    patient = models.ForeignKey(breast_craniofacial_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    procedure_name = models.CharField(max_length=100, verbose_name='نام روش جراحی')
    description = models.TextField(verbose_name='توضیحات جراحی')
    desired_results = models.TextField(verbose_name='نتایج مطلوب')
    risks_and_complications = models.TextField(verbose_name='مخاطرات و عوارض')
    recovery_time = models.PositiveIntegerField(verbose_name='زمان بازیابی پس از جراحی')
    postoperative_care = models.TextField(verbose_name='مراقبت پس از جراحی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"جراحی پلاستیک صورت سینه برای بیمار {self.patient.full_name}"

# مدل تجویز (breast_craniofacial_surgery_Treatment)
class breast_craniofacial_surgery_Treatment(models.Model):
    class Meta:
        db_table = 'breast_craniofacial_surgery_Treatment'
    patient = models.ForeignKey(breast_craniofacial_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    description = models.TextField(verbose_name='توضیحات تجویز')
    date = models.DateField(verbose_name='تاریخ تجویز')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"
