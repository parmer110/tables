# در فایل health_psychology/models.py

from django.db import models
from common.models import CommonModel

# تعریف متغیر جهانی name
name = "Health Psychology Specialist"

class HealthPsychologyPatient(CommonModel):
    # فیلدهای مدل Patient
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    # و سایر فیلدهای مورد نیاز

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class HealthPsychologyPrescription(CommonModel):
    # فیلدهای مدل دستورات پزشکی
    # مثلا:
    date = models.DateField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    # و سایر فیلدهای مورد نیاز

    def __str__(self):
        return f"Prescription - {self.date}"

class HealthPsychologyTest(CommonModel):
    # فیلدهای مدل آزمایش‌ها
    # مثلا:
    test_name = models.CharField(max_length=100)
    result = models.CharField(max_length=100)
    # و سایر فیلدهای مورد نیاز

    def __str__(self):
        return f"{self.test_name} - {self.result}"

class HealthPsychologyMedicalAction(CommonModel):
    # فیلدهای مدل نتایج اقدامات درمانی و پزشکی
    # مثلا:
    action_date = models.DateField()
    action_type = models.CharField(max_length=100)
    description = models.TextField()
    # و سایر فیلدهای مورد نیاز

    def __str__(self):
        return f"{self.action_type} - {self.action_date}"

class HealthPsychologyTreatment(CommonModel):
    # اطلاعات درمان‌های تخصص متخصص روان‌شناسی سلامت برای بیماران
    patient = models.ForeignKey(HealthPsychologyPatient, on_delete=models.CASCADE, related_name="treatments")
    treatment_date = models.DateField(verbose_name="تاریخ درمان")
    treatment_description = models.TextField(verbose_name="توضیحات درمان")
    # دیگر فیلدهای مربوط به درمان‌ها متخصص روان‌شناسی سلامت می‌توانند اضافه شوند

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name} - {self.treatment_date}"