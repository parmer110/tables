from django.db import models
from common.models import Person, Places, CommonModel

name="Emergency Medicine"

class emergency_medicine_Patient(CommonModel):
    class Meta:
        db_table = 'emergency_medicine_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class EmergencyComplaint(CommonModel):
    # فیلدهای مربوط به شکایت‌های اورژانسی بیمار
    name = models.CharField(max_length=100, verbose_name='نام شکایت')
    description = models.TextField(verbose_name='توضیحات شکایت')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class EmergencyProcedure(CommonModel):
    # فیلدهای مربوط به اقدامات اورژانسی
    name = models.CharField(max_length=100, verbose_name='نام اقدام')
    description = models.TextField(verbose_name='توضیحات اقدام')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class emergency_medicine_Treatment(CommonModel):
    class Meta:
        db_table = 'emergency_medicine_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(emergency_medicine_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند پزشکی اورژانس
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    chief_complaints = models.ManyToManyField(EmergencyComplaint, blank=True, verbose_name='شکایت‌های اورژانسی')
    initial_assessment = models.TextField(verbose_name='ارزیابی اولیه بیمار')
    emergency_procedures = models.ManyToManyField(EmergencyProcedure, blank=True, verbose_name='اقدامات اورژانسی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند پزشکی اورژانس بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
