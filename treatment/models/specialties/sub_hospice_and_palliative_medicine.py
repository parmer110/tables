from django.db import models

name = "Subspecialty Hospice and Palliative Medicine"

# مدل بیمار
class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

# مدل زیرتخصص بیمارستان و مراقبت‌های لطفاً (Hospice and Palliative Medicine)
class HospiceAndPalliativeMedicine(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    hospice_diagnosis = models.TextField(verbose_name='تشخیص بیمارستان')
    palliative_care_plan = models.TextField(verbose_name='طرح مراقبت‌های لطفاً')
    pain_management_plan = models.TextField(verbose_name='طرح مدیریت درد')
    symptom_management_plan = models.TextField(verbose_name='طرح مدیریت علائم')
    emotional_support = models.TextField(verbose_name='پشتیبانی عاطفی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"زیرتخصص بیمارستان و مراقبت‌های لطفاً برای بیمار {self.patient.full_name}"

# مدل تجویز (Treatment)
class Treatment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    description = models.TextField(verbose_name='توضیحات تجویز')
    date = models.DateField(verbose_name='تاریخ تجویز')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"
