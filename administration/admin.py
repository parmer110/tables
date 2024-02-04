from django.contrib import admin
from .models import *
# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    list_display=("pk", "name", "description")
    list_editable=("name", "description")
    
class CompanyWebsiteAdmin(admin.ModelAdmin):
    list_display=("id", "company")    
    list_editable=("company",)
    
admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyPersonRole)
admin.site.register(CompanyAddressRole)
admin.site.register(CompanyWebsite, CompanyWebsiteAdmin)