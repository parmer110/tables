from django.db import models
from common.models import Person, Places, CommonModel

name="Neurology"

class neurology_Patient(CommonModel):
    class Meta:
        db_table = 'neurology_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class NeurologicalSymptom(CommonModel):
    # فیلدهای مربوط به علائم عصبشناسی
    name = models.CharField(max_length=100, verbose_name='نام علامت عصبشناسی')
    description = models.TextField(verbose_name='توضیحات علامت عصبشناسی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class NeurologicalTest(CommonModel):
    # فیلدهای مربوط به آزمایش‌های عصبشناسی
    name = models.CharField(max_length=100, verbose_name='نام آزمایش عصبشناسی')
    description = models.TextField(verbose_name='توضیحات آزمایش عصبشناسی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class neurology_Treatment(CommonModel):
    class Meta:
        db_table = 'neurology_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(neurology_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند عصبشناسی
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    neurological_symptoms = models.ManyToManyField(NeurologicalSymptom, blank=True, verbose_name='علائم عصبشناسی')
    neurological_tests = models.ManyToManyField(NeurologicalTest, blank=True, verbose_name='آزمایش‌های عصبشناسی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند عصبشناسی بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
