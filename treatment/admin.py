from django.contrib import admin
from django.db import models
from .models.specialties.allergy_and_immunology import Allergy, ImmunologyTest, Treatment
from .models.models import Specialty

class SpecialtiesAdmin(admin.ModelAdmin):
    list_display=("id", "name", "class_name")

admin.site.register(Allergy)
admin.site.register(Specialty, SpecialtiesAdmin)