from django.db import models
from common.models import Person, Places, CommonModel
from common.models import Person, Places, CommonModel

name = "Allergy and Immunology"

class Allergy(CommonModel):
    # فیلدهای مربوط به آلرژی
    name = models.CharField(max_length=100, verbose_name='نام آلرژی')
    description = models.TextField(verbose_name='توضیحات آلرژی')
    #patient = models.ForeignKey(allergy_and_immunology_Patient, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    medications = models.TextField()

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class ImmunologyTest(CommonModel):
    # فیلدهای مربوط به آزمایش‌های ایمونولوژی
    name = models.CharField(max_length=100, verbose_name='نام آزمایش')
    #patient = models.ForeignKey(allergy_and_immunology_Patient, on_delete=models.CASCADE)
    laboratory_tests = models.TextField()
    hospitalization = models.BooleanField()
    surgery = models.BooleanField()
    post_treatment = models.TextField()
    result = models.CharField(max_length=100, verbose_name='نتیجه آزمایش')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return self.name

class allergy_and_immunology_Treatment(CommonModel):
    class Meta:
        db_table = 'allergy_and_immunology_Treatment'
    # بیمار مربوط به این روند درمانی
    patient = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='بیمار')

    # فیلدهای مربوط به روند درمانی
    visit_date = models.DateTimeField(verbose_name='تاریخ ویزیت')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    diagnosis = models.TextField(verbose_name='تشخیص بیماری')
    prescriptions = models.TextField(verbose_name='دستورات پزشک')
    paraclinical_tests = models.ManyToManyField(ImmunologyTest, blank=True, verbose_name='آزمایش‌های ایمونولوژی')
    allergies = models.ManyToManyField(Allergy, blank=True, verbose_name='آلرژی‌ها')
    hospitalization = models.BooleanField(default=False, verbose_name='بستری شده؟')
    surgery = models.TextField(blank=True, null=True, verbose_name='جراحی و اقدامات جراحی')
    post_treatment = models.TextField(blank=True, null=True, verbose_name='اقدامات بعد از درمان')

    # سایر فیلدهای مورد نیاز می‌توانند افزوده شوند

    def __str__(self):
        return f"روند درمانی بیمار {self.patient.full_name} در تاریخ {self.visit_date}"