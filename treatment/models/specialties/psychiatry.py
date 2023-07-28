from django.db import models

name = "Psychiatry"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class PsychiatricTreatment(models.Model):
    # فیلدهای مربوط به روش‌های درمانی روانپزشکی
    name = models.CharField(max_length=100, verbose_name='نام روش درمانی روانپزشکی')
    description = models.TextField(verbose_name='توضیحات روش درمانی روانپزشکی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class PsychiatricTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های روانپزشکی
    name = models.CharField(max_length=100, verbose_name='نام آزمایش روانپزشکی')
    description = models.TextField(verbose_name='توضیحات آزمایش روانپزشکی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند روانپزشکی
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    psychiatric_treatments = models.ManyToManyField(PsychiatricTreatment, blank=True, verbose_name='روش‌های درمانی روانپزشکی')
    psychiatric_tests = models.ManyToManyField(PsychiatricTest, blank=True, verbose_name='آزمایش‌های روانپزشکی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند روانپزشکی بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
