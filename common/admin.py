from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.db import models
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "token_lifetime", "password", "email", "is_active", "display_groups", "display_permissions")
    list_editable = ("email", "token_lifetime" )

    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    display_groups.short_description = "Groups"

    def display_permissions(self, obj):
        return ", ".join([perm.name for perm in obj.user_permissions.all()])
    display_permissions.short_description = "Permissions"

class PersonAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "firstname", "lastname", "gender", "date_of_birth", "mobile_phone", 'email', "national_code", 'get_address')
    # filter_horizontal = ('address',)
    # list_editable = ("_gender",)
    def get_address(self, obj):
        return ", ".join([place.city for place in obj.address.all()])
    
    get_address.short_description = 'Address'    
    formfield_overrides = {
        models.TextField: {'widget': admin.widgets.AdminTextareaWidget(attrs={'rows': 1})},
    }
    class Media:
        css = {
            'all': ('css/custom_admin.css',),
        }

class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'city', 'region', 'longitude', 'latitude', 'gps_longitude', 'gps_latitude')

class PlacesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "country", "state", "city", "address", "postalcode", "phoneNumber", "usage", "manager")
    list_editable = ("manager",)


class SiteManagementLogAdmin(admin.ModelAdmin):
      
    list_display=("id", "ip4", "ip6", "link", "action")

class TranslateAdmin(admin.ModelAdmin):
    list_display=("id", "persian", "english", "arabic", "russian", "chineseTraditional", "spanish", "french", "german", "italian")
    # list_editable=("persian", "english", "arabic", "russian", "chineseTraditional", "spanish")
    formfield_overrides = {
        models.TextField: {'widget': admin.widgets.AdminTextareaWidget(attrs={'rows': 1})},
    }
    class Media:
        css = {
            'all': ('css/custom_admin.css',),
        }

class SystemSettingsPicAdmin(admin.ModelAdmin):
    list_display=("id", "company", "app", "name", "max_image_size_width", "max_image_size_height", "max_image_file_size_mb", "allowed_image_formats")
    list_editable=("app", "company", "name", "max_image_size_width", "max_image_size_height", "max_image_file_size_mb", "allowed_image_formats")

class PicturesAdmin(admin.ModelAdmin):
    list_display=("id", "image_settings", "name", "description", "image")
    list_editable=("image_settings", "name", "description", "image")
    

class EducationalDegreeAdmin(admin.ModelAdmin):
    list_display=("id", "name", "abbreviation", "description", "duration_years")
    # list_editable=("name", "abbreviation", "description", "duration_years")

class ClassificationAdmin(admin.ModelAdmin):
    list_display=("id", "app", "model", "name", "sub_class", "type", "description")
    # list_editable=("app", "model", "name", "sub_class", "type", "description")

class FieldOfStudyAdmin(admin.ModelAdmin):
    list_display=("id", "name", "classification", "description")
    # list_editable=("name", "classification", "description")

class AcademicCategoryAdmin(admin.ModelAdmin):
    list_display=("id", "name", "description")
    # list_editable=("name", "description")

class AcademicRankAdmin(admin.ModelAdmin):
    list_display=("id", "name", "description")

class LegalTypesAdmin(admin.ModelAdmin):
    list_display=("id", "name", "description")
    list_editable=("name", "description")

class LegalEntityAdmin(admin.ModelAdmin):
    list_display=("id", "name", "type", "classification", "registration_number", "contact_email", "contact_phone")
    list_editable=("name", "type", "classification", "registration_number", "contact_email", "contact_phone")


class AppModelsAdmin(admin.ModelAdmin):
    list_display = ("id", "application", "model", "description")
    list_editable = ("application", "model", "description")

class SettingMenusAdmin(admin.ModelAdmin):
    list_display=("id", "index", "name", "parent", "cat", "path", "container_tag", "is_active")
    list_editable=("index", "name", "parent", "cat", "path", "container_tag", "is_active")

class SettingAdmin(admin.ModelAdmin):
    list_display=("id", "company", "application", "page", "model",)
    list_editable=("company", "application", "page", "model",)


class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "ipv4_address", "ipv6_address", "action", "timestamp", "content_type", "object_id")

class MyCounterAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "value")
 
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'expire_date', 'session_data')

class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "app_label", "model")


class TokenLifetimeAdmin(admin.ModelAdmin):
    list_display = ("id", "lifetime")
    list_editable = ("lifetime",)

class LoginRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "ipv4_address", "ipv6_address", "ip_validation_status", "login_date_time", "user_agent_data", "device_type", "location", "gps_location")

class UserSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "session_key", "session_data", "login_time", "logout_time", "device_type", "location")


admin.site.register(User, UserAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Places, PlacesAdmin)
admin.site.register(SiteManagementLog, SiteManagementLogAdmin)
admin.site.register(Translate, TranslateAdmin)
admin.site.register(SystemSettingsPic, SystemSettingsPicAdmin)
admin.site.register(Pictures, PicturesAdmin)
admin.site.register(EducationalDegree, EducationalDegreeAdmin)
admin.site.register(Classification, ClassificationAdmin)
admin.site.register(FieldOfStudy, FieldOfStudyAdmin)
admin.site.register(AcademicCategory, AcademicCategoryAdmin)
admin.site.register(AcademicRank, AcademicRankAdmin)
admin.site.register(LegalTypes, LegalTypesAdmin)
admin.site.register(LegalEntity, LegalEntityAdmin)
admin.site.register(AppModels, AppModelsAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(SettingMenus, SettingMenusAdmin)
admin.site.register(Jobs)
admin.site.register(JobRoles)
admin.site.register(AuditLog, AuditLogAdmin)
admin.site.register(MyCounter, MyCounterAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(ContentType, ContentTypeAdmin)
admin.site.register(TokenLifetime, TokenLifetimeAdmin)
admin.site.register(LoginRecord, LoginRecordAdmin)
admin.site.register(UserSession, UserSessionAdmin)