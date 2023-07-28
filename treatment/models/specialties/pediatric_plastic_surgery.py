from django.db import models

class Patient(models.Model):
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

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند جراحی پلاستیک کودکان
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    pediatric_plastic_surgery_procedures = models.ManyToManyField(PediatricPlasticSurgeryProcedure, blank=True, verbose_name='روش‌های جراحی پلاستیک کودکان')
    pediatric_plastic_surgery_tests = models.ManyToManyField(PediatricPlasticSurgeryTest, blank=True, verbose_name='آزمایش‌های جراحی پلاستیک کودکان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی پلاستیک کودکان بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
