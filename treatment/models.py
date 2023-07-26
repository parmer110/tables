from django.db import models
from common.utils.crypto import encoder, decoder
from common.models import Person, Places, CommonModel

class SellRepresentation(CommonModel):
    name = models.CharField(max_length=255, blank=True, null=True)

class Customer(CommonModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birthrate = models.IntegerField(blank=True, null=True)

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
