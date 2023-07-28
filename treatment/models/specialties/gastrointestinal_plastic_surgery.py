from django.db import models
from common.models import Person, Places, CommonModel

name = "Subspecialty Gastrointestinal Plastic Surgery"

class gastrointestinal_plastic_surgery_Patient(models.Model):
    class Meta:
        db_table = 'gastrointestinal_plastic_surgery_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن بیمار')
    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class GastrointestinalPlasticSurgery(models.Model):
    # بیمار مربوط به جراحی پلاستیک گوارشی
    patient = models.ForeignKey(gastrointestinal_plastic_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # نوع جراحی پلاستیک گوارشی
    surgery_type = models.CharField(max_length=100, verbose_name='نوع جراحی پلاستیک گوارشی')

    # تاریخ جراحی پلاستیک گوارشی
    surgery_date = models.DateField(verbose_name='تاریخ جراحی پلاستیک گوارشی')

    # توضیحات دیگر مرتبط با جراحی پلاستیک گوارشی
    description = models.TextField(verbose_name='توضیحات جراحی پلاستیک گوارشی')
    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"جراحی پلاستیک گوارشی برای بیمار {self.patient.full_name}"

class gastrointestinal_plastic_surgery_Treatment(models.Model):
    class Meta:
        db_table = 'gastrointestinal_plastic_surgery_Treatment'
    # بیمار مربوط به تجویز
    patient = models.ForeignKey(gastrointestinal_plastic_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # تاریخ تجویز
    prescription_date = models.DateField(verbose_name='تاریخ تجویز')

    # نام دارو یا درمان
    medication_name = models.CharField(max_length=100, verbose_name='نام دارو یا درمان')

    # دوز دارو یا درمان
    dosage = models.CharField(max_length=50, verbose_name='دوز دارو یا درمان')

    # توضیحات مربوط به تجویز
    description = models.TextField(verbose_name='توضیحات تجویز')
    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"

