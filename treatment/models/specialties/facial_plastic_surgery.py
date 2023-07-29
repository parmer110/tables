from django.db import models
from common.models import Person, Places, CommonModel

name = "Facial Plastic Surgery"

class facial_plastic_surgery_Patient(CommonModel):
    class Meta:
        db_table = 'facial_plastic_surgery_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class FacialPlasticSurgeryProcedure(CommonModel):
    # فیلدهای مربوط به روش‌های جراحی پلاستیک صورت
    name = models.CharField(max_length=100, verbose_name='نام روش جراحی پلاستیک صورت')
    description = models.TextField(verbose_name='توضیحات روش جراحی پلاستیک صورت')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class FacialPlasticSurgeryTest(CommonModel):
    # فیلدهای مربوط به آزمایش‌های جراحی پلاستیک صورت
    name = models.CharField(max_length=100, verbose_name='نام آزمایش جراحی پلاستیک صورت')
    description = models.TextField(verbose_name='توضیحات آزمایش جراحی پلاستیک صورت')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class facial_plastic_surgery_Treatment(CommonModel):
    class Meta:
        db_table = 'facial_plastic_surgery_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(facial_plastic_surgery_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند جراحی پلاستیک صورت
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    facial_plastic_surgery_procedures = models.ManyToManyField(FacialPlasticSurgeryProcedure, blank=True, verbose_name='روش‌های جراحی پلاستیک صورت')
    facial_plastic_surgery_tests = models.ManyToManyField(FacialPlasticSurgeryTest, blank=True, verbose_name='آزمایش‌های جراحی پلاستیک صورت')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند جراحی پلاستیک صورت بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
