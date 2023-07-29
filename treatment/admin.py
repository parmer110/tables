from django.contrib import admin
from django.db import models
from .models.models import Specialty

class SpecialtiesAdmin(admin.ModelAdmin):
    list_display=("id", "name", "class_name")

admin.site.register(Specialty, SpecialtiesAdmin)