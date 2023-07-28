from django.db import models

name = "Adult Oncology"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class AdultOncologyProcedure(models.Model):
    # فیلدهای مربوط به روش‌های جراحی آنکولوژی بالغین
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی آنکولوژی بالغین')
    description = models.TextField(verbose_name='توضیحات روش جراحی آنکولوژی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class AdultOncologyTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های آنکولوژی بالغین
    name = models.CharField(max_length=100, verbose_name='نام آزمایش آنکولوژی بالغین')
    description = models.TextField(verbose_name='توضیحات آزمایش آنکولوژی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند آنکولوژی بالغین
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    adult_oncology_procedures = models.ManyToManyField(AdultOncologyProcedure, blank=True, verbose_name='روش‌های جراحی آنکولوژی بالغین')
    adult_oncology_tests = models.ManyToManyField(AdultOncologyTest, blank=True, verbose_name='آزمایش‌های آنکولوژی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند آنکولوژی بالغین بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
