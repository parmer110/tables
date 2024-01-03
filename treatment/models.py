import os
from importlib import import_module
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from common.utils.crypto import encoder, decoder
from common.utils.tools import load_specialty_module
from common.models import Person, Places, CommonModel, Document, Schedule, Location, Classification, Rating, AcademicRecord, EducationalDegree
from administration.models import Company
from financialhub.models import Cost

class Qualification(CommonModel):
    qualification_name = models.CharField(max_length=200)
    institute_name = models.CharField(max_length=200, null=True, blank=True)
    university = models.CharField(max_length=100, null=True, blank=True)
    procurement_year = models.DateField()
    certification_date = models.DateField(null=True)
    certification_expires = models.DateField(null=True)
    evidence = models.OneToOneField(Document, on_delete=models.SET_NULL, null=True, blank=True)
    document = models.ManyToManyField(Document, related_name="common_qualification")


class Translator(CommonModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="treatment_translator")
    classification = models.ForeignKey(Classification, on_delete=models.SET_NULL, related_name="appointment_translator", null=True, blank=True)
    languages = models.CharField(max_length=200)
    rating = models.ManyToManyField(Rating, related_name="treatment_translator", blank=True)
    history = models.TextField(null=True)
    cost = models.ForeignKey(Cost, on_delete=models.SET_NULL, related_name="translator", null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Specialty(CommonModel):
    name = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=50, verbose_name="مخفف تخصص")
    description = models.TextField(null=True)
    degree = models.ForeignKey(EducationalDegree, on_delete=models.CASCADE, verbose_name="مدرک تخصص")
    is_active = models.BooleanField(default=True)
        
    class Meta:
        verbose_name = "Specialty"
        verbose_name_plural = "Specialties"

    def __str__(self):
        return f"{self.name} (" + "ACTIVATED" if self.is_active else "Inactive"


class SubSpecialty(CommonModel):
    name = models.CharField(max_length=200, verbose_name="نام فوق‌تخصص", unique=True)    
    abbreviation = models.CharField(max_length=20, verbose_name="مخفف فوق‌تخصص")
    description = models.TextField(verbose_name="توضیحات")
    degree = models.ForeignKey(EducationalDegree, on_delete=models.CASCADE, verbose_name="مدرک فوق‌تخصص")
    parent_specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name="sub_specialties", verbose_name="تخصص مادر")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (" + "ACTIVATED" if self.is_active else "Inactive"


class Procedure(CommonModel):
    name = models.CharField(max_length=200, verbose_name="نام فرآیند درمانی", unique=True)
    code = models.IntegerField(unique=True)
    description = models.TextField(verbose_name="توضیحات", null=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='medical_procedures', blank=True, null=True, verbose_name="تخصص مرتبط")
    subspecialty = models.ForeignKey(SubSpecialty, on_delete=models.CASCADE, related_name="medical_procedure", blank=True, null=True, verbose_name="زیرتخصص مرتبط")
    skills = models.TextField(verbose_name="مهارت‌ها", null=True)
    cost = models.ForeignKey(Cost, on_delete=models.SET_NULL, related_name="treatment_procedure", verbose_name="هزینه (در واحد پولی)", null=True)
    classification = models.ManyToManyField(Classification, related_name="procedure")
    is_active = models.BooleanField(default=True)

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="procedure", null=True)
    qualification = models.ForeignKey(Qualification, on_delete=models.SET_NULL, null=True)
    head = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)
    physician = models.ManyToManyField('Physician', related_name="procedure_company")
    nurse = models.ManyToManyField('nursing.Nurses', related_name="procedure_company")

    def __str__(self):
        return f"{self.name} (" + "ACTIVATED" if self.is_active else "Inactive"


class MedicalCenter(CommonModel):
    name = models.CharField(verbose_name="نام مرکز درمانی", max_length=100)
    address = models.ForeignKey(Places, on_delete=models.SET_NULL, related_name="medical_center", verbose_name="نام مرکز درمانی", null=True)
    specialties = models.ManyToManyField(Specialty, blank=True, through="MedicalCenterSpecialty", related_name="medical_center")
    managers = models.ManyToManyField(Person, through="MedicalCenterPerson", blank=True, related_name="medical_center_managers")
    schedule = models.ManyToManyField(Schedule, through="MedicalCenterSchedule", related_name="medical_center")
    website = models.URLField(blank=True, null=True, verbose_name="آدرس وبسایت")
    email = models.EmailField(blank=True, null=True, verbose_name="ایمیل مرکز درمانی")
    rating = models.FloatField(default=0, verbose_name="امتیاز مرکز درمانی")
    classification = models.ForeignKey(Classification, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="طبقه‌بندی")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, related_name="treatment_medical_center", null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "مرکز درمانی"
        verbose_name_plural = "مراکز درمانی"


class MedicalCenterSpecialty(CommonModel):
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name="throught_medical_center_specialty")
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name="medical_center_specialty")
    credentials = models.OneToOneField(Document, on_delete=models.SET_NULL, null=True, blank=True)

class MedicalCenterPerson(CommonModel):
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name="throught_medical_center_person")
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="medical_center_person")
    evidence = models.OneToOneField(Document, on_delete=models.SET_NULL, null=True, blank=True)

class MedicalCenterSchedule(CommonModel):
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name="throught_medical_center_schedule")
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="medical_center_schedule")
    cost_coefficient = models.DecimalField(max_digits=5, decimal_places=2, default=1.0, verbose_name="Cost Coefficient")

class MedicalCenterUnit(CommonModel):
    medical_center = models.ManyToManyField(MedicalCenter, verbose_name="Medical Center", through="MedicalCenterUnitMedicalCenter")
    name = models.CharField(max_length=100, verbose_name="Unit Name")
    description = models.TextField(verbose_name="Desctiption")
    schedule = models.ManyToManyField(Schedule, through="MedicalCenterUnitSchedule")
    head = models.ForeignKey("Physician", on_delete=models.SET_NULL, null=True)
    physician = models.ManyToManyField('Physician', related_name="medical_center_unit")
    nurses = models.ManyToManyField("nursing.Nurses", related_name="medical_center_unit")
    classification = models.ForeignKey(Classification, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="طبقه‌بندی")
    cost = models.ForeignKey(Cost, on_delete=models.SET_NULL, related_name="treatment_medical_center_unit", verbose_name="هزینه (در واحد پولی)", null=True)

class MedicalCenterUnitMedicalCenter(CommonModel):
    medical_center_unit = models.ForeignKey(MedicalCenterUnit, on_delete=models.CASCADE)
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE)
    number_of_rooms = models.PositiveIntegerField(verbose_name="Number of Rooms")
    number_of_beds = models.PositiveIntegerField(verbose_name="Number of Beds")
    specialty = models.ManyToManyField(Specialty, verbose_name="Specialty", through="MedicalCenterUnitMedicalCenterSpecialty")
    rating = models.IntegerField(default=0, verbose_name="Rating")
    classification = models.ForeignKey(Classification, on_delete=models.SET_NULL, related_name="medical_center_unit_medical_center", null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, related_name="medical_center_unit_medical_center", null=True)

class MedicalCenterUnitSchedule(CommonModel):
    medical_center_unit = models.ForeignKey(MedicalCenterUnit, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    is_open = models.BooleanField(default=True, verbose_name="Is Open")

class MedicalCenterUnitMedicalCenterSpecialty(CommonModel):
    medical_center_unit_medical_center = models.ForeignKey(MedicalCenterUnitMedicalCenter, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, verbose_name="Rating")
    classification = models.CharField(max_length=100, blank=True, null=True, verbose_name="Classification")


class Physician(CommonModel):
    person = models.OneToOneField(Person, on_delete=models.SET_NULL, null=True)
    medical_degree = models.ForeignKey(AcademicRecord, on_delete=models.CASCADE, related_name="physicians")
    specialties = models.ManyToManyField(Specialty, through='PhysicianSpecialty')
    subspecialty = models.ManyToManyField(SubSpecialty, blank=True, related_name="physicain")
    procedure = models.ManyToManyField(Procedure, through="PhysicianProcedure", related_name="Physician")
    medical_center = models.ManyToManyField(MedicalCenter, through="PhysicianMedicalCenter", blank=True, related_name="physician")
    trained_in = models.ForeignKey('TrainedIn', on_delete=models.SET_NULL, related_name="physician_trained_in", null=True)
    license_number = models.CharField(max_length=20, unique=True)
    graduation_date = models.DateField()
    qualification = models.ManyToManyField(Qualification, related_name="physician")
    documentation = models.ManyToManyField(Document, blank=True, related_name="physician")
    cost = models.ForeignKey(Cost, on_delete=models.SET_NULL, related_name="treatment_physician", verbose_name="هزینه (در واحد پولی)", null=True)

    def __str__(self):
        return f"physician {self.person.firstname} {self.person.lastname}"

class PhysicianSpecialty(CommonModel):
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    qualification = models.OneToOneField(Qualification, on_delete=models.SET_NULL, related_name="physician_specialty", null=True)
    
    def __str__(self):
        return f'{self.physician} - {self.specialty}'

class PhysicianProcedure(CommonModel):
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    qualification = models.ForeignKey(Qualification, on_delete=models.SET_NULL, related_name="physician_procedure", null=True)

    def __str__(self):
        return f'{self.physician} - {self.procedure}'

class PhysicianMedicalCenter(CommonModel):
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE)
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE)
    credentials = models.OneToOneField(Document, on_delete=models.SET_NULL, null=True, blank=True)


class Office(CommonModel):
    address = models.ForeignKey(Places, on_delete=models.CASCADE, related_name="treatment_office")
    physician = models.ForeignKey(Physician, on_delete=models.SET_NULL, related_name="office", null=True)
    specialty = models.ManyToManyField(Specialty, related_name="office_specialty")
    time_slot_per_client_in_min = models.IntegerField()
    first_consultation_fee = models.ManyToManyField(Cost, blank=True, related_name="office_first_consultation_fee")
    followup_consultation_fee = models.ManyToManyField(Cost, blank=True, related_name="office_followup_consultation_fee")


class OfficePhysicianAvailability(CommonModel):
    schedule = models.ManyToManyField(Schedule, related_name="treatment_office_physician_availability")
    office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name="office_availability")
    is_available = models.BooleanField()
    reason_of_unavailability = models.TextField()


class TreatmentPackage(CommonModel):
    name = models.CharField(max_length=200, null=True)
    classification = models.ManyToManyField(Classification, related_name="treatment_package", blank=True)
    description = models.TextField(null=True)
    specialties = models.ManyToManyField(Specialty)
    medical_center = models.ManyToManyField(MedicalCenter, through="treatment_package_medical_center", related_name="treatment_package", blank=True)
    physicians = models.ManyToManyField(Physician, related_name="treatment_package")
    treatment_duration = models.DurationField(null=True)
    cost = models.ManyToManyField(Cost, related_name="treatment_treatment_package")
    model_documentation = models.ManyToManyField(Document, related_name="treatment_package", blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
            verbose_name = "Treatment"
            verbose_name_plural = "Treatments"

class treatment_package_medical_center(CommonModel):
    treatment_package = models.ForeignKey(TreatmentPackage, on_delete=models.CASCADE)
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE)


class MedicalHistory(CommonModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Customer')
    treatment_package = models.ForeignKey('treatment.TreatmentPackage', on_delete=models.CASCADE, verbose_name='Treatment Package', null=True, blank=True)
    medical_center = models.ManyToManyField(MedicalCenter,  related_name="medical_history", verbose_name="Medical Center")
    physician = models.ManyToManyField(Physician, related_name="medical_history", verbose_name="Physician")
    details = models.TextField(verbose_name="Details")
    document = models.OneToOneField(Document, on_delete=models.SET_NULL, null=True, blank=True)
    treatment_year = models.PositiveIntegerField(verbose_name='Treatment Year')

    def __str__(self):
        return f'{self.person} - {self.treatment_package} - {self.treatment_year}'

    class Meta:
        verbose_name = 'Medical History'
        verbose_name_plural = 'Medical Histories'


class Customer(CommonModel):
    person = models.OneToOneField(Person, on_delete=models.SET_NULL, related_name="treatment_patient", null=True)
    medical_history = models.ManyToManyField(MedicalHistory, through="CustomerMedicalHistory", related_name="customer")

    def __str__(self):
        return f"{self.person.firstname} {self.person.lastname}"


class CustomerMedicalHistory(CommonModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    medical_history = models.ForeignKey(MedicalHistory, on_delete=models.CASCADE)


class SellRepresentation(CommonModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="sell_representation")
    specialties = models.ManyToManyField(Specialty, related_name="sell_representation")
    organization_value = models.PositiveIntegerField(default=0, verbose_name="ارزش سازمانی")
    professional_fields = models.TextField(verbose_name="حوزه‌های حرفه‌ای", null=True)
    credentials = models.ManyToManyField(Document, blank=True, related_name="sell_representation_credentials")
    evidence = models.ManyToManyField(Document, blank=True, related_name="sell_representation_evidence")
    summary = models.TextField(blank=True, null=True, verbose_name="خلاصه اطلاعات")

    def __str__(self):
        return f"{self.person.firstname} {self.person.lastname}"

    class Meta:
        verbose_name = "نماینده‌ی فروش"
        verbose_name_plural = "نمایندگان فروش"
        # ordering = ['-rank', 'name'] 

class SalesCommission(CommonModel):
    sell_representation = models.ForeignKey(SellRepresentation, on_delete=models.CASCADE)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    amount_earned = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.sell_representation} - Commission: {self.commission_percentage}%"        

class SalesFeedback(CommonModel):
    sell_representation = models.ForeignKey(SellRepresentation, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    rank = models.PositiveIntegerField(default=0, verbose_name="رتبه")
    feedback_text = models.TextField()

    def __str__(self):
        return f"{self.sell_representation} - Rating: {self.rating}"


class Patient(CommonModel):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True)
    insuranceid = models.IntegerField()
    pcp = models.IntegerField() # Primary Care Physician

    class Meta:
        db_table = 'treatment_Patient'


class Order(CommonModel):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, related_name="order", null=True)
    treatment_packages = models.ManyToManyField(TreatmentPackage, related_name="order", verbose_name="درمان", blank=True)
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.SET_NULL, related_name="order", verbose_name="مرکز درمانی", null=True)
    physician = models.ForeignKey(Physician, on_delete=models.SET_NULL, related_name="order", verbose_name="پزشک", null=True)
    sell_representation = models.ForeignKey(SellRepresentation, on_delete=models.SET_NULL, verbose_name="نماینده فروش", null=True)
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت سفارش", null=True)
    appointment_date = models.DateTimeField(verbose_name="تاریخ و زمان ملاقات", null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مجموع هزینه", null=True)
    cost = models.ManyToManyField(Cost, related_name="treatment_order")
    is_paid = models.BooleanField(default=False, verbose_name="پرداخت شده؟", null=True)
    status = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"Order {self.pk} - Customer: {self.customer.person.firstname} {self.customer.person.lastname}"

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"
        ordering = ['-order_date']


class Clinic(CommonModel):
    name = models.CharField(max_length=255, verbose_name="نام کلینیک", null=True)
    healthCenter = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name="clinic")
    specialties = models.ManyToManyField(Specialty, related_name="clinic")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return F"Clinic {self.name}"

    class Meta:
        verbose_name = "کلینیک"
        verbose_name_plural = "کلینیک‌ها"


class ParaClinic(CommonModel):
    name = models.CharField(max_length=255, verbose_name="نام پاراکلینیک", null=True)
    healthCenter = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name="paraClinic")
    specialties = models.ManyToManyField(Specialty, related_name="para_clinic")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return F"ParaClinic {self.name}"

    class Meta:
        verbose_name = "پاراکلینیک"
        verbose_name_plural = "پاراکلینیک‌ها"


class Hospital(CommonModel):
    name = models.CharField(max_length=255, verbose_name="نام بیمارستان", null=True)
    healthCenter = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name="hospital")
    specialties = models.ManyToManyField(Specialty)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return F"Hospital {self.name}"


class TrainedIn(CommonModel):
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name="trainedIn", null=True)
    physician = models.ManyToManyField(Physician, related_name="trained_in_physician")
    specialty = models.ManyToManyField(Specialty, related_name="trained_in_specialty")
    certificationdate = models.DateField()
    certificationexpires = models.DateField()
    documents = models.ManyToManyField(Document, related_name="trained_in_document", blank=True)


class Block(CommonModel):
    name = models.CharField(max_length=100)
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name="block", null=True)
    medical_center_unit = models.ForeignKey(MedicalCenterUnit, on_delete=models.CASCADE, related_name="block", null=True, blank=True)
    blockfloor = models.IntegerField()
    blockcode = models.IntegerField()
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Room(CommonModel):
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name="room", null=True)
    medical_center_unit = models.ForeignKey(MedicalCenterUnit, on_delete=models.CASCADE, related_name="room", null=True, blank=True)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name="room", null=True)
    roomnumber = models.IntegerField(unique=True)
    roomtype = models.ForeignKey(Classification, on_delete=models.SET_NULL, related_name="medical_center_room", null=True)
    blockfloor = models.IntegerField()
    blockcode = models.IntegerField()
    unavailable = models.BooleanField()



class Stay(CommonModel):
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name="stay", null=True)
    medical_center_unit = models.ForeignKey(MedicalCenterUnit, on_delete=models.CASCADE, related_name="stay", null=True, blank=True)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name="stay", null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    stayid = models.IntegerField(unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="medical_center_stay", null=True)
    schedule = models.ManyToManyField(Schedule, related_name="treatment_stay")
    admit_date = models.DateTimeField()
    discharge_date = models.DateTimeField()

    def __str__(self):
        return f"{self.patient.customer.person.firstname} - Block: {self.patient.customer.person.lastname}-{self.block.block_code}"


class AppBookingChannel(CommonModel):
    app_booking_channel_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.app_booking_channel_name

    class Meta:
        verbose_name = "App Booking Channel"
        verbose_name_plural = "App Booking Channels"


class AppointmentStatus(CommonModel):
    status = models.CharField(max_length=10)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = "Appointment Status"
        verbose_name_plural = "Appointment Statuses"
        

class Appointment(CommonModel):
    description = models.TextField(blank=True, null=True)
    app_booking_channel = models.ForeignKey(AppBookingChannel, on_delete=models.SET_NULL, related_name="appointment", null=True)
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name="appointment", null=True)
    examination_room = models.ManyToManyField(MedicalCenterUnit, related_name="treatment_appointment", blank=True)
    physician = models.ForeignKey(Physician, on_delete=models.SET_NULL, related_name="appointment", null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointment", null=True)
    prep_nurse = models.ForeignKey("nursing.Nurses", on_delete=models.CASCADE, null=True)
    translator = models.ManyToManyField(Translator, related_name="appointment", blank=True)
    appointment_date = models.DateTimeField(null=True)
    probable_start_time = models.ForeignKey(Schedule, on_delete=models.SET_NULL, related_name="appointment_probable_start_time", null=True)
    actual_end_time = models.ForeignKey(Schedule, on_delete=models.SET_NULL, related_name="appointment_actual_end_time", null=True)
    appointment_schedule = models.ForeignKey(Schedule, on_delete=models.SET_NULL, related_name="appointment", null=True)
    visit_details = models.TextField(blank=True, null=True)
    is_surgery = models.BooleanField(default=False)
    surgery_details = models.TextField(blank=True, null=True)
    is_recurring = models.BooleanField(default=False)
    recurring_frequency = models.PositiveIntegerField(default=0, help_text="Frequency of recurring appointments in days (0 for non-recurring)")
    appointment_status = models.ForeignKey(AppointmentStatus, on_delete=models.SET_NULL, related_name="appointment", null=True)
    appointmen_documentation = models.ForeignKey(Document, on_delete=models.SET_NULL, related_name="treatment_appointment", null=True, blank=True,)

    def __str__(self):
        return f"{self.patient.person.name} - {self.appointment_date}"

    class Meta:
        ordering = ['-appointment_date']


class Service(CommonModel):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

class ServiceAppointment(CommonModel):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.appointment} - {self.service.name}"


class Prescribes(CommonModel):
    physician = models.ForeignKey(Physician, on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="prescribes")
    medication = models.IntegerField()
    date = models.DateTimeField()
    appointment = models.IntegerField()
    dose = models.CharField(max_length=255)


class HospitalAffiliation(CommonModel):
    Physician = models.ForeignKey(Physician, on_delete=models.CASCADE, related_name="hospital_affiliation", null=True)
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name="hospital_affiliation", null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)


class AffiliatedWith(CommonModel):
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name="affiliated_with", null=True)
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE, related_name="affiliated_with", null=True)
    department = models.ForeignKey(MedicalCenterUnit, on_delete=models.CASCADE, related_name="affiliated_with", null=True)
    primaryaffiliation = models.BooleanField()


class SurgerySimulator(CommonModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    manufacturer = models.CharField(max_length=100)
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.SET_NULL, related_name="surgery_simulator", null=True)
    specification = models.ManyToManyField(Specialty, related_name="surgery_simulator")
    physician = models.ManyToManyField(Physician, related_name="surgery_simulator")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Surgery Simulator"
        verbose_name_plural = "Surgery Simulators"


class MedicalPlan(CommonModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="medical_plan", null=True)
    schedule = models.ManyToManyField(Schedule, related_name="treatment_medical_plan")
    description = models.TextField()

    def __str__(self):
        return f"{self.patient.name}'s Medical Plan"


class Treatment(CommonModel):
    medical_plan = models.ForeignKey(MedicalPlan, on_delete=models.CASCADE, related_name="treatment", null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.ForeignKey(Schedule, on_delete=models.SET_NULL, related_name="treatment_treatment", null=True)
    cost = models.ManyToManyField(Cost, through="TreatmentCost", related_name="treatment_treatment")
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Treatment"
        verbose_name_plural = "Treatments"

    def __str__(self):
        return self.name


class TreatmentCost(CommonModel):
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, related_name="treatment_cost", null=True)
    cost = models.ForeignKey(Cost, on_delete=models.CASCADE, related_name="treatment_treatmentcost", null=True)
    # Registers each costs date.


class OveralMedication(CommonModel):
    medical_plan = models.ForeignKey(MedicalPlan, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MedicalRecord(CommonModel):
    status_history = models.TextField(blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    admission_date = models.DateTimeField()
    discharge_date = models.DateTimeField(blank=True, null=True)
    diagnosis = models.TextField()
    prescribed_medications = models.ManyToManyField(OveralMedication)
    medical_center = models.ManyToManyField(MedicalCenter, blank=True)
    attending_physician = models.ManyToManyField(Physician, related_name="medical_records")
    content = models.TextField()

    def add_status_history(self, status):
        if self.status_history:
            self.status_history += f"\n{status} - {timezone.now()}"
        else:
            self.status_history = f"{status} - {timezone.now()}"
        self.save()

    def __str__(self):
        return f"Medical Record - ID: {self.pk}"


__all__ = ['Qualification', 'Translator', 'Specialty', 'SubSpecialty', 'Procedure', 'MedicalCenter', 'MedicalCenterUnit', 'Physician', 
'Office', 'TreatmentPackage', 'MedicalHistory', 'Customer', 'SellRepresentation', 'SalesCommission','SalesFeedback', 'Patient', 'Order', 
'Clinic', 'ParaClinic', 'Hospital']


# class test(models.Model):
#     n1 = models.ForeignKey(load_specialty_module('treatment.models.specialties.allergy_and_immunology').Allergy, on_delete=models.CASCADE)
