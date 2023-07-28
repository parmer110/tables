from django.db import models

name = "Breast Cosmetic Surgery"

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

# مدل تخصص جراحی پلاستیک تجمیلی سینه (Breast Cosmetic Surgery)
class BreastCosmeticSurgery(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    procedure_name = models.CharField(max_length=100, verbose_name='نام روش جراحی')
    description = models.TextField(verbose_name='توضیحات جراحی')
    implant_type = models.CharField(max_length=100, verbose_name='نوع ایمپلنت')
    implant_size = models.CharField(max_length=50, verbose_name='اندازه ایمپلنت')
    incision_type = models.CharField(max_length=100, verbose_name='نوع برش جراحی')
    recovery_time = models.PositiveIntegerField(verbose_name='زمان بازیابی پس از جراحی')
    postoperative_care = models.TextField(verbose_name='مراقبت پس از جراحی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"جراحی پلاستیک تجمیلی سینه برای بیمار {self.patient.full_name}"

# مدل تجویز (Treatment)
class Treatment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    description = models.TextField(verbose_name='توضیحات تجویز')
    date = models.DateField(verbose_name='تاریخ تجویز')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"