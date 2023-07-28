from django.db import models

name = "Burn Surgery"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class BurnSeverity(models.Model):
    # فیلدهای مربوط به شدت سوختگی
    name = models.CharField(max_length=100, verbose_name='نام شدت سوختگی')
    description = models.TextField(verbose_name='توضیحات شدت سوختگی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class BurnSurgeryProcedure(models.Model):
    # فیلدهای مربوط به روش‌های جراحی پلاستیک سوختگی
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی پلاستیک سوختگی')
    description = models.TextField(verbose_name='توضیحات روش جراحی پلاستیک سوختگی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به شدت سوختگی
    burn_severity = models.ForeignKey(BurnSeverity, on_delete=models.CASCADE, verbose_name='شدت سوختگی')

    # فیلدهای مربوط به روند جراحی پلاستیک سوختگی
    burn_surgery_procedures = models.ManyToManyField(BurnSurgeryProcedure, blank=True, verbose_name='روش‌های جراحی پلاستیک سوختگی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی پلاستیک سوختگی بیمار {self.patient.full_name} با شدت سوختگی {self.burn_severity}"
