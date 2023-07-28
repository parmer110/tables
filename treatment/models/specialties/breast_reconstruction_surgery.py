from django.db import models
from common.models import Person, Places, CommonModel

name = "Breast Reconstruction Surgery"

# مدل بیمار
class breast_reconstruction_surgery_Patient(models.Model):
    class Meta:
        db_table = 'breast_reconstruction_surgery_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

# مدل تخصص جراحی پلاستیک ترمیمی سینه (Breast Reconstruction Surgery)
class BreastReconstructionSurgery(models.Model):
    patient = models.ForeignKey(breast_reconstruction_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    technique_name = models.CharField(max_length=100, verbose_name='نام تکنیک جراحی ترمیمی سینه')
    description = models.TextField(verbose_name='توضیحات تکنیک جراحی ترمیمی سینه')
    duration_minutes = models.PositiveIntegerField(verbose_name='مدت زمان جراحی (دقیقه)')
    success_rate = models.FloatField(verbose_name='نرخ موفقیت در جراحی')
    reconstruction_material = models.CharField(max_length=100, verbose_name='مواد ترمیمی سینه')
    complications = models.TextField(verbose_name='ممکن است طی جراحی پیش آید')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تکنیک جراحی ترمیمی سینه بیمار {self.patient.full_name}"

# مدل تجویز (breast_reconstruction_surgery_Treatment)
class breast_reconstruction_surgery_Treatment(models.Model):
    class Meta:
        db_table = 'breast_reconstruction_surgery_Treatment'
    patient = models.ForeignKey(breast_reconstruction_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    description = models.TextField(verbose_name='توضیحات تجویز')
    date = models.DateField(verbose_name='تاریخ تجویز')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"
