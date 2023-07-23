from django.contrib import admin
from django.db import models
from .models import User, Person

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "timestamp")

class PersonAdmin(admin.ModelAdmin):
    list_display=("id", "firstname", "lastname", "sex", "birthdate", "address", "mobile_phone", "national_code")
    formfield_overrides = {
        models.TextField: {'widget': admin.widgets.AdminTextareaWidget(attrs={'rows': 1})},
    }
    class Media:
        css = {
            'all': ('css/custom_admin.css',),
        }


admin.site.register(User, UserAdmin)
admin.site.register(Person, PersonAdmin)