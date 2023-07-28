from django.db import models

name="Pathology"

class Patient(models.Model):
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class PathologyFinding(models.Model):
    # فیلدهای مربوط به یافته‌های پاتولوژی
    name = models.CharField(max_length=100, verbose_name='نام یافته پاتولوژی')
    description = models.TextField(verbose_name='توضیحات یافته پاتولوژی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class PathologyTest(models.Model):
    # فیلدهای مربوط به آزمایش‌های پاتولوژی
    name = models.CharField(max_length=100, verbose_name='نام آزمایش پاتولوژی')
    description = models.TextField(verbose_name='توضیحات آزمایش پاتولوژی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class Treatment(models.Model):
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند پاتولوژی
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    pathology_findings = models.ManyToManyField(PathologyFinding, blank=True, verbose_name='یافته‌های پاتولوژی')
    pathology_tests = models.ManyToManyField(PathologyTest, blank=True, verbose_name='آزمایش‌های پاتولوژی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند پاتولوژی بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
