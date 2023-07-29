from django.db import models
from common.models import Person, Places, CommonModel

name="Family Medicine"

class family_medicine_Patient(CommonModel):
    class Meta:
        db_table = 'family_medicine_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class FamilyHealthIssue(CommonModel):
    # فیلدهای مربوط به مسائل سلامت خانواده
    name = models.CharField(max_length=100, verbose_name='نام مسئله سلامت')
    description = models.TextField(verbose_name='توضیحات مسئله سلامت')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class HealthCheckup(CommonModel):
    # فیلدهای مربوط به چک‌آپ سلامتی خانواده
    date = models.DateField(verbose_name='تاریخ چک‌آپ')
    results = models.TextField(verbose_name='نتایج چک‌آپ')
    family_health_issues = models.ManyToManyField(FamilyHealthIssue, blank=True, verbose_name='مسائل سلامت خانواده')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"چک‌آپ سلامتی خانواده در تاریخ {self.date}"

class family_medicine_Treatment(CommonModel):
    class Meta:
        db_table = 'family_medicine_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(family_medicine_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند پزشکی خانواده
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    chief_complaints = models.TextField(verbose_name='شکایت‌های اصلی بیمار')
    diagnosis = models.TextField(verbose_name='تشخیص بیماری')
    health_checkups = models.ManyToManyField(HealthCheckup, blank=True, verbose_name='چک‌آپ‌های سلامتی خانواده')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند پزشکی خانواده بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
