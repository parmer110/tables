from django.db import models
from common.models import CommonModel, Person, Places, Schedule
from financialhub.models import Cost


class Accommodation(CommonModel):
    name = models.CharField(max_length=200)
    schedule = models.ManyToManyField(Schedule, related_name="accommodation", blank=True)
    description = models.TextField()
    contact_person = models.ForeignKey(Person, on_delete=models.CASCADE,related_name="accommodation_contact")
    price_per_night = models.ForeignKey(Cost, on_delete=models.SET_NULL, related_name="accommodation", null=True)
    hotel = models.ManyToManyField('Hotel', related_name="hotel", blank=True)
    Suite = models.ManyToManyField('Suite', related_name="hotel", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Accommodation'
        verbose_name_plural = 'Accommodations'


class Hotel(CommonModel):
    name = models.CharField(max_length=200)
    address = models.ForeignKey(Places, on_delete=models.CASCADE, related_name="hotel", null=True)
    contact_person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    facilities = models.TextField(blank=True, null=True)
    capacity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotels'


class Suite(CommonModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.ForeignKey(Places, on_delete=models.CASCADE, related_name="suite", null=True)
    contact_person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Suite'
        verbose_name_plural = 'Suites'
