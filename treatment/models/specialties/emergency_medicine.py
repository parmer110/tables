from django.db import models

name="Emergency Medicine"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class EmergencyComplaint(models.Model):
    # فیلدهای مربوط به شکایت‌های اورژانسی بیمار
    name = models.CharField(max_length=100, verbose_name='نام شکایت')
    description = models.TextField(verbose_name='توضیحات شکایت')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class EmergencyProcedure(models.Model):
    # فیلدهای مربوط به اقدامات اورژانسی
    name = models.CharField(max_length=100, verbose_name='نام اقدام')
    description = models.TextField(verbose_name='توضیحات اقدام')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند پزشکی اورژانس
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    chief_complaints = models.ManyToManyField(EmergencyComplaint, blank=True, verbose_name='شکایت‌های اورژانسی')
    initial_assessment = models.TextField(verbose_name='ارزیابی اولیه بیمار')
    emergency_procedures = models.ManyToManyField(EmergencyProcedure, blank=True, verbose_name='اقدامات اورژانسی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند پزشکی اورژانس بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
