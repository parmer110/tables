from django.db import models
from common.models import Person, Places, CommonModel

class pediatric_plastic_surgery_Patient(models.Model):
    class Meta:
        db_table = 'pediatric_plastic_surgery_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class PediatricPlasticSurgeryProcedure(models.Model):
    # فیلدهای مربوط به روش‌های جراحی پلاستیک کودکان
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی پلاستیک کودکان')
    description = models.TextField(verbose_name='توضیحات روش جراحی پلاستیک کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class PediatricPlasticSurgeryTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های جراحی پلاستیک کودکان
    name = models.CharField(max_length=100, verbose_name='نام آزمایش جراحی پلاستیک کودکان')
    description = models.TextField(verbose_name='توضیحات آزمایش جراحی پلاستیک کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class pediatric_plastic_surgery_Treatment(models.Model):
    class Meta:
        db_table = 'pediatric_plastic_surgery_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(pediatric_plastic_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند جراحی پلاستیک کودکان
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    pediatric_plastic_surgery_procedures = models.ManyToManyField(PediatricPlasticSurgeryProcedure, blank=True, verbose_name='روش‌های جراحی پلاستیک کودکان')
    pediatric_plastic_surgery_tests = models.ManyToManyField(PediatricPlasticSurgeryTest, blank=True, verbose_name='آزمایش‌های جراحی پلاستیک کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی پلاستیک کودکان بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
