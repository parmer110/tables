from django.db import models
from common.models import CommonModel, Person, Places, Document
# from treatment.models.models import Patient, Specialty, MedicalCenter, Qualification


class Nurses(CommonModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    # specialties = models.ManyToManyField("treatment.Specialty", through="NursesSpecialty")
    # medical_center = models.ManyToManyField("treatment.MedicalCenter", through="NursesMedicalCenter", blank=True, related_name="nurses")
    position = models.CharField(max_length=255)
    qualification = models.CharField(max_length=100)
    registered = models.BooleanField()

    def __str__(self):
        return f"Nurse, {self.person.firstname} {self.person.lastname}"

    class Meta:
        verbose_name = 'Nurse'
        verbose_name_plural = 'Nurses'


class NursesSpecialty(CommonModel):
    nurse = models.ForeignKey(Nurses, on_delete=models.CASCADE, related_name="nurse_specialty")
    # specialty = models.ForeignKey("treatment.Specialty", on_delete=models.CASCADE, related_name="nurse_specialty")
    # qualification = models.OneToOneField("treatment.Qualification", on_delete=models.SET_NULL, related_name="nurse_specialty", null=True)

class NursesMedicalCenter(CommonModel):
    nurse = models.ForeignKey(Nurses, on_delete=models.CASCADE)
    # medical_center = models.ForeignKey("treatment.MedicalCenter", on_delete=models.CASCADE)
    credentials = models.OneToOneField(Document, on_delete=models.SET_NULL, null=True, blank=True)


class NursingService(CommonModel):
    # patient = models.ForeignKey("treatment.Patient", on_delete=models.CASCADE, null=True)
    nurse = models.ForeignKey(Nurses, on_delete=models.CASCADE, null=True)
    service_type = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.service_type} for {self.patient}'

    class Meta:
        verbose_name = 'Nursing Service'
        verbose_name_plural = 'Nursing Services'
