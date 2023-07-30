from django import forms
from django.contrib import admin
from django.db import models
from django.contrib.postgres.fields import ArrayField
from .models.models import Specialty, SellRepresentation
from .models.specialties.__constants import choices1, choices2, choices3

class SpecialtiesAdmin(admin.ModelAdmin):
    list_display=("id", "name", "class_name")

class SellRepresentationForm(forms.ModelForm):
    specialties = forms.MultipleChoiceField(choices=choices3, required=False)

    class Meta:
        model = SellRepresentation
        fields = '__all__'

class SellRepresentationAdmin(admin.ModelAdmin):
    form = SellRepresentationForm
    list_display = ("id", "person", "specialties")
    list_editable = ("person", "specialties")

admin.site.register(SellRepresentation, SellRepresentationAdmin)
admin.site.register(Specialty, SpecialtiesAdmin)