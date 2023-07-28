from django.db import models

name = "Physical Medicine and Rehabilitation"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class PhysicalRehabilitationProcedure(models.Model):
    # فیلدهای مربوط به روش‌های پزشکی فیزیکال و توانبخشی
    name = models.CharField(max_length=100, verbose_name='نام روش پزشکی فیزیکال و توانبخشی')
    description = models.TextField(verbose_name='توضیحات روش پزشکی فیزیکال و توانبخشی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class RehabilitationTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های پزشکی فیزیکال و توانبخشی
    name = models.CharField(max_length=100, verbose_name='نام آزمایش پزشکی فیزیکال و توانبخشی')
    description = models.TextField(verbose_name='توضیحات آزمایش پزشکی فیزیکال و توانبخشی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند پزشکی فیزیکال و توانبخشی
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    physical_rehabilitation_procedures = models.ManyToManyField(PhysicalRehabilitationProcedure, blank=True, verbose_name='روش‌های پزشکی فیزیکال و توانبخشی')
    rehabilitation_tests = models.ManyToManyField(RehabilitationTest, blank=True, verbose_name='آزمایش‌های پزشکی فیزیکال و توانبخشی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند پزشکی فیزیکال و توانبخشی بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
