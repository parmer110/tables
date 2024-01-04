from django import forms
from django.contrib import admin
from django.db import models
from django.contrib.postgres.fields import ArrayField
from .models import *

class SpecialtiesAdmin(admin.ModelAdmin):
    list_display=("id", "name", "abbreviation", "description", "degree", "is_active")

class SellRepresentationForm(forms.ModelForm):
    specialties = forms.MultipleChoiceField(required=False)

    class Meta:
        model = SellRepresentation
        fields = '__all__'

class SellRepresentationAdmin(admin.ModelAdmin):
    form = SellRepresentationForm
    list_display = ("id", "person",)
    list_editable = ("person",)

# class MedicalDegreeAdmin(admin.ModelAdmin):
#     list_display = ("id", "name", "category", "abbreviation", "description", "duration_years")
#     list_editable = ("category","duration_years")

class ProcedureAdmin(admin.ModelAdmin):
    list_display=("id", "name", "code", "description", "specialty", "subspecialty", "skills", "is_active", "company")
    # list_editable=("name", "code", "description", "specialty", "subspecialty", "skills", "is_active", "company")
    list_editable=("company",)

admin.site.register(SellRepresentation, SellRepresentationAdmin)
admin.site.register(Specialty, SpecialtiesAdmin)
admin.site.register(Procedure, ProcedureAdmin)