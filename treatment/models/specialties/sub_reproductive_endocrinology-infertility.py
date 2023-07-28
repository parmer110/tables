from django.db import models

name = "Subspecialty Reproductive Endocrinology/Infertility"

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

# مدل زیرتخصص پزشکی غدد و ناباروری تولید مثل (Reproductive Endocrinology/Infertility)
class ReproductiveEndocrinology(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    hormonal_disorders = models.TextField(verbose_name='اختلالات هورمونی')
    infertility_diagnosis = models.TextField(verbose_name='تشخیص ناباروری')
    treatment_options = models.TextField(verbose_name='گزینه‌های درمانی')

    # فیلدهای مربوط به زیرتخصص غدد و ناباروری تولید مثل
    # ...

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"زیرتخصص پزشکی غدد و ناباروری تولید مثل برای بیمار {self.patient.full_name}"

# مدل تجویز (Treatment)
class Treatment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')
    description = models.TextField(verbose_name='توضیحات تجویز')
    date = models.DateField(verbose_name='تاریخ تجویز')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"تجویز برای بیمار {self.patient.full_name}"
