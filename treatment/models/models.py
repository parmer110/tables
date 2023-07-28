import os
from importlib import import_module
from django.db import models
from common.utils.crypto import encoder, decoder
from common.models import Person, Places, CommonModel


class SellRepresentation(CommonModel):
    person = models.CharField(max_length=255, blank=True, null=True)
    

class Customer(CommonModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="patient")
    medical_history = models.TextField()

    def __str__(self):
        return self.person.name
class Order(CommonModel):
    pass

class TreatmentPackage(CommonModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="treatmentPackage")
    pass
class HealthCenter(CommonModel):
    treatmentPackage = models.ForeignKey(TreatmentPackage, on_delete=models.CASCADE, related_name="healthCenter")

class Clinic(CommonModel):
    healthCenter = models.ForeignKey(HealthCenter, on_delete=models.CASCADE, related_name="healthCenter")

class ParaClinic(CommonModel):
    healthCenter = models.ForeignKey(HealthCenter, on_delete=models.CASCADE, related_name="paraClinic")

class Hospital(CommonModel):
    healthCenter = models.ForeignKey(HealthCenter, on_delete=models.CASCADE, related_name="hospital")

class Procedure(CommonModel):
    Hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="procedure")
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    cost = models.FloatField()

class TrainedIn(CommonModel):
    Hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="trainedIn")
    physician = models.IntegerField()
    treatment = models.IntegerField()
    certificationdate = models.DateField()
    certificationexpires = models.DateField()

class Room(CommonModel):
    roomnumber = models.IntegerField(unique=True)
    roomtype = models.CharField(max_length=255)
    blockfloor = models.IntegerField()
    blockcode = models.IntegerField()
    unavailable = models.BooleanField()

class Stay(CommonModel):
    stayid = models.IntegerField(unique=True)
    patient = models.IntegerField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class Nurse(CommonModel):
    employeeid = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    registered = models.BooleanField()
    ssn = models.IntegerField()

class AffiliatedWith(CommonModel):
    physician = models.IntegerField()
    department = models.IntegerField()
    primaryaffiliation = models.BooleanField()

class Prescribes(CommonModel):
    physician = models.IntegerField()
    patient = models.IntegerField()
    medication = models.IntegerField()
    date = models.DateTimeField()
    appointment = models.IntegerField()
    dose = models.CharField(max_length=255)

class Patient(CommonModel):
    ssn = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=255)
    insuranceid = models.IntegerField()
    pcp = models.IntegerField()

class Appointment(CommonModel):
    id = models.AutoField(primary_key=True)
    user_account_id = models.IntegerField()  # Foreign key to user account
    office_id = models.IntegerField()  # Foreign key to office
    probable_start_time = models.DateTimeField()
    actual_end_time = models.DateTimeField(blank=True, null=True)
    appointment_status_id = models.IntegerField()  # Foreign key to appointment status
    appointment_taken_date = models.DateField()
    app_booking_channel_id = models.IntegerField()  # Foreign key to app booking channel

class AppointmentStatus(CommonModel):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10)

class AppBookingChannel(CommonModel):
    id = models.AutoField(primary_key=True)
    app_booking_channel_name = models.CharField(max_length=255)

class Specialization(CommonModel):
    id = models.AutoField(primary_key=True)
    specialization_name = models.CharField(max_length=100)

class DoctorSpecialization(CommonModel):
    id = models.AutoField(primary_key=True)
    doctor = models.IntegerField()
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)

class Doctor(CommonModel):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    professional_statement = models.TextField()
    practicing_from = models.DateField()

class Qualification(CommonModel):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    qualification_name = models.CharField(max_length=200)
    institute_name = models.CharField(max_length=200)
    procurement_year = models.DateField()

class HospitalAffiliation(CommonModel):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

class Specialty(models.Model):

    spec_module_path = 'treatment.models'
    spec_packages = [name for name in os.listdir(os.path.dirname(__file__)) if os.path.isdir(os.path.join(os.path.dirname(__file__), name)) and not name.startswith('__')]

    choices1 = [(package, package) for package in spec_packages]


    choices2 = []
    spec_module_path = 'treatment.models.specialties'
    spec_module = import_module(spec_module_path)
    spec_files = os.listdir(os.path.dirname(spec_module.__file__))
    for spec_file in spec_files:
        if spec_file.endswith('.py') and not spec_file.startswith('__'):
            spec_module_name = os.path.splitext(spec_file)[0]
            spec_module = import_module(f'{spec_module_path}.{spec_module_name}')
            choices2.append((spec_module.name, spec_module_name))


    choices3 = []
    spec_module_path = 'treatment.models.specialties'
    spec_module = import_module(spec_module_path)
    spec_files = os.listdir(os.path.dirname(spec_module.__file__))
    
    for spec_file in spec_files:
        if spec_file.endswith('.py') and not spec_file.startswith('__'):
            spec_module_name = os.path.splitext(spec_file)[0]
            spec_module = import_module(f'{spec_module_path}.{spec_module_name}')
            choices3.append((getattr(spec_module, 'name'), getattr(spec_module, 'name')))

    branches = models.CharField(max_length=100, choices=choices1, null=True)
    class_name = models.CharField(max_length=100, choices=choices2)
    name = models.CharField(max_length=100, choices=choices3)
    
    def __str__(self):
        return self.name