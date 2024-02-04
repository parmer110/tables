from django.db import models
from common.models import CommonModel, Person, Places, LegalEntity, JobRoles, Document, Path


class Employee(CommonModel):
    user = models.OneToOneField(Person, on_delete=models.CASCADE, null=True)
    job_title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.job_title}'

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'


class InternalMessage(CommonModel):
    sender = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver}'

    class Meta:
        verbose_name = 'Internal Message'
        verbose_name_plural = 'Internal Messages'


class CompanyPersonRole(CommonModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="company_person_role", null=True)
    job_role = models.ForeignKey(JobRoles, on_delete=models.CASCADE, related_name="company_person_role", null=True)

    def __str__(self):
        return f"{self.person.firstname} {self.person.lastname} role is {self.job_role.name}"

class CompanyAddressRole(CommonModel):
    address = models.ForeignKey(Places, on_delete=models.CASCADE, related_name="company_address_role", null=True)
    job_role = models.ForeignKey(JobRoles, on_delete=models.CASCADE, related_name="company_adress_role", null=True)

    def __str__(self):
        return f"{self.address.title} role is {self.job_role.name}"

class Company(CommonModel):
    name = models.CharField(max_length=30, verbose_name="Company Name", null=True, unique=True)
    legal_entity = models.ForeignKey(LegalEntity, on_delete=models.CASCADE, null=True)
    personnel_roles = models.ManyToManyField(CompanyPersonRole, related_name='companies')
    address_roles = models.ManyToManyField(CompanyAddressRole, related_name='companies')
    description = models.TextField(null=True)
    document = models.ManyToManyField(Document, blank=True)

    def __str__(self):
        return f"{self.legal_entity} {self.name}"



class CompanyWebsite(CommonModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_websites")
    url = models.ManyToManyField(Path, related_name='company_websites')

    def __str__(self):
        return str(self.url)