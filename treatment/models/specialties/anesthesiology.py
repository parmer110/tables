from django.db import models

name = "Anesthesiology"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class AnesthesiaType(models.Model):
    # فیلدهای مربوط به نوع بیهوشی
    name = models.CharField(max_length=100, verbose_name='نوع بیهوشی')
    description = models.TextField(verbose_name='توضیحات نوع بیهوشی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class AnesthesiaComplication(models.Model):
    # فیلدهای مربوط به عوارض بیهوشی
    name = models.CharField(max_length=100, verbose_name='نام عارضه')
    description = models.TextField(verbose_name='توضیحات عارضه')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند بیهوشی
    anesthesia_type = models.ForeignKey(AnesthesiaType, on_delete=models.PROTECT, verbose_name='نوع بیهوشی')
    anesthesia_start_time = models.DateTimeField(verbose_name='زمان شروع بیهوشی')
    anesthesia_end_time = models.DateTimeField(verbose_name='زمان پایان بیهوشی')
    anesthesia_complications = models.ManyToManyField(AnesthesiaComplication, blank=True, verbose_name='عوارض بیهوشی')
    medications = models.TextField(verbose_name='داروهای مصرفی در بیهوشی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند بیهوشی بیمار {self.patient.full_name} در تاریخ {self.anesthesia_start_time}"
