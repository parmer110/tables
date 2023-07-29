from django.db import models
from common.models import Person, Places, CommonModel

name="Nuclear Medicine"

class nuclear_medicine_Patient(CommonModel):
    class Meta:
        db_table = 'nuclear_medicine_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class NuclearMedicineProcedure(CommonModel):
    # فیلدهای مربوط به روش‌های پزشکی هسته‌ای
    name = models.CharField(max_length=100, verbose_name='نام روش پزشکی هسته‌ای')
    description = models.TextField(verbose_name='توضیحات روش پزشکی هسته‌ای')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class NuclearMedicineTest(CommonModel):
    # فیلدهای مربوط به آزمایش‌های پزشکی هسته‌ای
    name = models.CharField(max_length=100, verbose_name='نام آزمایش پزشکی هسته‌ای')
    description = models.TextField(verbose_name='توضیحات آزمایش پزشکی هسته‌ای')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class nuclear_medicine_Treatment(CommonModel):
    class Meta:
        db_table = 'nuclear_medicine_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(nuclear_medicine_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند پزشکی هسته‌ای
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    nuclear_medicine_procedures = models.ManyToManyField(NuclearMedicineProcedure, blank=True, verbose_name='روش‌های پزشکی هسته‌ای')
    nuclear_medicine_tests = models.ManyToManyField(NuclearMedicineTest, blank=True, verbose_name='آزمایش‌های پزشکی هسته‌ای')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند پزشکی هسته‌ای بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
