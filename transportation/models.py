from django.db import models
from common.models import CommonModel, Person, Places, Classification
from treatment.models import Customer
from financialhub.models import Cost

class Vehicle(CommonModel):
    name = models.CharField(max_length=255)
    vehicle_type = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'


class TransportReservation(CommonModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()

    def __str__(self):
        return f'Transport Reservation for {self.customer}'

    class Meta:
        verbose_name = 'Transport Reservation'
        verbose_name_plural = 'Transport Reservations'


class FlightBook(CommonModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="transportation_flightbook")
    origin_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    departure_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    ticket_number = models.CharField(max_length=50, unique=True)
    airline = models.CharField(max_length=100)
    flight_class = models.CharField(max_length=20)
    price = models.ManyToManyField(Cost, related_name="transportation_flightbook", blank=True)
    status = models.ForeignKey(Classification, on_delete=models.SET_NULL, related_name="transportation_flightbook", null=True)
    # models.CharField(max_length=20, choices=[
    #     ('confirmed', 'Confirmed'),
    #     ('pending', 'Pending'),
    #     ('canceled', 'Canceled'),
    # ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.person.firstname} {self.customer.person.lastname}- {self.ticket_number}"