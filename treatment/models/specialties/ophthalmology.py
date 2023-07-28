from django.db import models

name="Ophthalmology"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class EyeCondition(models.Model):
    # فیلدهای مربوط به شرایط چشمی
    name = models.CharField(max_length=100, verbose_name='نام شرایط چشمی')
    description = models.TextField(verbose_name='توضیحات شرایط چشمی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class OphthalmologyTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های چشم پزشکی
    name = models.CharField(max_length=100, verbose_name='نام آزمایش چشم پزشکی')
    description = models.TextField(verbose_name='توضیحات آزمایش چشم پزشکی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند چشم پزشکی
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    eye_conditions = models.ManyToManyField(EyeCondition, blank=True, verbose_name='شرایط چشمی')
    ophthalmology_tests = models.ManyToManyField(OphthalmologyTest, blank=True, verbose_name='آزمایش‌های چشم پزشکی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند چشم پزشکی بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
