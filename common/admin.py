from django.contrib import admin
from .models import User, Person

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "timestamp")

class PersonAdmin(admin.ModelAdmin):
    list_display=("id", "firstname", "lastname")

admin.site.register(User, UserAdmin)
admin.site.register(Person, PersonAdmin)