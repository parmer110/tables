from django.db import models
from common.models import Person, Places, CommonModel

name = "Urogenital Plastic Surgery"

class urogenital_plastic_surgery_Patient(models.Model):
    class Meta:
        db_table = 'urogenital_plastic_surgery_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن بیمار')
    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class UrogenitalPlasticSurgery(models.Model):
    # بیمار مربوط به جراحی پلاستیک ادراری
    patient = models.ForeignKey(urogenital_plastic_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # نوع جراحی پلاستیک ادراری
    surgery_type = models.CharField(max_length=100, verbose_name='نوع جراحی پلاستیک ادراری')

    # تاریخ جراحی پلاستیک ادراری
    surgery_date = models.DateField(verbose_name='تاریخ جراحی پلاستیک ادراری')

    # توضیحات دیگر مرتبط با جراحی پلاستیک ادراری
    description = models.TextField(verbose_name='توضیحات جراحی پلاستیک ادراری')
    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"جراحی پلاستیک ادراری برای بیمار {self.patient.full_name}"

class urogenital_plastic_surgery_Treatment(models.Model):
    class Meta:
        db_table = 'urogenital_plastic_surgery_Treatment'
    # بیمار مربوط به تجویز
    patient = models.ForeignKey(urogenital_plastic_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

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

