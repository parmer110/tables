from django.db import models
from common.models import Person, Places, CommonModel

name = "Adult Nephrology"

class adult_nephrology_Patient(CommonModel):
    class Meta:
        db_table = 'adult_nephrology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class AdultNephrologyProcedure(CommonModel):
    # فیلدهای مربوط به روش‌های نفرولوژی بالغین
    name = models.CharField(max_length=100, verbose_name='نام روش نفرولوژی بالغین')
    description = models.TextField(verbose_name='توضیحات روش نفرولوژی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class AdultNephrologyTest(CommonModel):
    # فیلدهای مربوط به آزمایش‌های نفرولوژی بالغین
    name = models.CharField(max_length=100, verbose_name='نام آزمایش نفرولوژی بالغین')
    description = models.TextField(verbose_name='توضیحات آزمایش نفرولوژی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class adult_nephrology_Treatment(CommonModel):
    class Meta:
        db_table = 'adult_nephrology_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(adult_nephrology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند نفرولوژی بالغین
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    adult_nephrology_procedures = models.ManyToManyField(AdultNephrologyProcedure, blank=True, verbose_name='روش‌های نفرولوژی بالغین')
    adult_nephrology_tests = models.ManyToManyField(AdultNephrologyTest, blank=True, verbose_name='آزمایش‌های نفرولوژی بالغین')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند نفرولوژی بالغین بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
