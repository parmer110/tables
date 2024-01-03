from django.db import models
from common.models import Person, Places, CommonModel
from treatment.models import Customer


class TouristAttraction(CommonModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.ForeignKey(Places, on_delete=models.CASCADE, related_name="tourism_tourism_attraction")
    image = models.ImageField(upload_to='tourist_attractions/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tourist Attraction'
        verbose_name_plural = 'Tourist Attractions'


class Tour(CommonModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    attractions = models.ManyToManyField(TouristAttraction)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'Tour for {self.customer}'

    class Meta:
        verbose_name = 'Tour'
        verbose_name_plural = 'Tours'

