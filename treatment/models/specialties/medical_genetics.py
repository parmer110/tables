from django.db import models
from common.models import Person, Places, CommonModel

name="Medical Genetics"

class medical_genetics_Patient(models.Model):
    class Meta:
        db_table = 'medical_genetics_Patient'
    # فیلدهای مربوط به بیمار
    full_name = models.CharField(max_length=100, verbose_name='نام کامل بیمار')
    age = models.PositiveIntegerField(verbose_name='سن')
    phone = models.CharField(max_length=15, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.full_name

class GeneticDisorder(models.Model):
    # فیلدهای مربوط به اختلالات ژنتیکی
    name = models.CharField(max_length=100, verbose_name='نام اختلال ژنتیکی')
    description = models.TextField(verbose_name='توضیحات اختلال ژنتیکی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class GeneticTest(models.Model):
    # فیلدهای مربوط به آزمایشات ژنتیکی
    name = models.CharField(max_length=100, verbose_name='نام آزمایش ژنتیکی')
    description = models.TextField(verbose_name='توضیحات آزمایش ژنتیکی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class medical_genetics_Treatment(models.Model):
    class Meta:
        db_table = 'medical_genetics_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(medical_genetics_Patient, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند ژنتیک پزشکی
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    genetic_disorders = models.ManyToManyField(GeneticDisorder, blank=True, verbose_name='اختلالات ژنتیکی')
    genetic_tests = models.ManyToManyField(GeneticTest, blank=True, verbose_name='آزمایشات ژنتیکی')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند ژنتیک پزشکی بیمار {self.patient.full_name} در تاریخ {self.visit_date}"
