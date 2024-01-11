import os
from django.conf import settings
from django.urls import resolve, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpRequest
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import IntegrityError, models
from django.core.validators import RegexValidator
from django.views import View
import json
from django.apps import apps
from django.db.models import Q, Prefetch
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, UntypedToken
from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework_simplejwt.authentication import JWTAuthentication
from common.authentication import BlacklistJWTAuthentication
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from jwt import decode, InvalidTokenError
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError, TokenError
from rest_framework import viewsets, serializers as drf_serializers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status
from django.core.exceptions import ValidationError
from django.core import serializers
import ipaddress
from django.contrib.auth.models import Permission
from django_user_agents.utils import get_user_agent
import pytz
from user_agents import parse
from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError
import geoip2.database
from rest_framework.throttling import AnonRateThrottle
import logging
from django.utils.decorators import method_decorator
from django.core.cache import cache
# from celery.result import AsyncResult
from django.http import HttpResponseNotAllowed
from django.contrib.contenttypes.models import ContentType
from .tasks import fetch_related_data
from .forms import ImageForm, Register, CustomAuthenticationForm
from .models import Pictures, SettingMenus, User, LoginRecord, UserSession, Location, AppModels, UserProfile, UserRole
from administration.models import CompanyWebsite
from .utils.tools import (
    get_app_names, has_group,
    check_blacklist, blacklist_token, create_new_token, delete_expired_tokens, real_token_lifetimes,
    extract_ip_data, extract_user_agent_data, 
    get_location_data, extract_geo_data,
    generate_unique_session_key, custom_authenticate, check_token_func,
)
from .decorators.permissions import check_token
from .serializers import serialize_model
from .pagination import StandardResultsSetPagination
from .utilities import conditional_cache_page
from .permissions import CustomModelPermission


logger = logging.getLogger(__name__)

def in_group_admin(user):
    return user.groups.filter(name='admin').exists()

@api_view(['POST'])
@authentication_classes([BlacklistJWTAuthentication])
@permission_classes([IsAuthenticated])
def set_session(request, key, value):
    if not check_token_func(request):
        return JsonResponse({"error": "Authentication error!"}, status=400)
    if request.method != "POST":
        return JsonResponse({"error": "POST request requited."}, status=400)
    if key in ['page', 'tag']:
        request.session[key] = value
        return JsonResponse({'status': 'success'}, status=201)

@api_view(['GET', 'POST'])
@authentication_classes([BlacklistJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_session(request, key):
    if not check_token_func(request):
        return JsonResponse({"error": "Authentication error!"}, status=400)
    if key in ['page', 'tag']:
        value = request.session.get(key, None)
        return JsonResponse({'value': value})


        # try:
        #     response = super().post(request, data=data)
        # except Exception as e:
        #     print(e)
        #     return Response("Error occurred: " + str(e), status=400)


class CustomTokenRefreshView(TokenRefreshView, APIView):

    def post(self, request):

        refresh_token = request.COOKIES.get('refresh_token')
        access_token = request.COOKIES.get('access_token')
        
        if not (refresh_token and access_token):
            return Response("Authentication error!", status=400)

        try:
            decode(refresh_token, options={"verify_signature": False})
            decode(access_token, options={"verify_signature": False})
        except InvalidTokenError:
            return Response("Authentication error!", status=400)
        
        # data = {'refresh': refresh_token}
        request.data['refresh'] = refresh_token
        
        response = super().post(request)
        
        new_access_token = response.data['access']
        new_refresh_token = response.data['refresh']

        if not (new_access_token and new_refresh_token):
            return Response("Authentication error!", status=400)
            # return  HttpResponseRedirect(reverse('login'))
        
        new_access_lifetime_seconds = AccessToken(new_access_token).lifetime.total_seconds()
        new_refresh_lifetime_seconds = RefreshToken(new_refresh_token).lifetime.total_seconds()

        response.set_cookie('access_token', new_access_token,  max_age=new_access_lifetime_seconds, httponly=True, secure=True, samesite='Lax')
        response.set_cookie('access_token_expiry', new_access_lifetime_seconds)
        response.set_cookie('refresh_token', new_refresh_token, max_age=new_refresh_lifetime_seconds, httponly=True, secure=True, samesite='Lax')
        response.set_cookie('refresh_token_expiry', new_refresh_lifetime_seconds)
        print(f"↓↓{request.user}↓↓")
        return response


class SettingMenusTablesIndexViewSet(viewsets.ModelViewSet):

    authentication_classes = [BlacklistJWTAuthentication]
    permission_classes = [IsAuthenticated, CustomModelPermission]

    queryset = SettingMenus.objects.all()
    serializer_class = serialize_model(AppModels, ['id'])

    under_develope = settings.DEVELOPMENT_MODE
    
    def retrieve(self, request, *args, **kwargs):
        page = request.query_params.get('page', 1)
        version = settings.VERSION
        
        # Caching 
        if not self.under_develope:
            cache_key = f"setting_table_index_view_set_retrieve_{kwargs['pk']}_page_{page}:{version}"
            cached_data = cache.get(cache_key)

            if cached_data is not None:
                return Response(cached_data)

        instance = self.get_object()
        many_to_many_field = instance.tables.all()
        
        viewable_models = [
            model for model in many_to_many_field 
            if request.user.has_perm(
                f"{model.application.lower()}.view_{model.model.lower()}"
            )
        ]
        paginator = StandardResultsSetPagination(page_size=3)
        paginated_field = paginator.paginate_queryset(viewable_models, request)
        if paginated_field is not None:
            serializer = self.get_serializer(paginated_field, many=True)
            response = paginator.get_paginated_response(serializer.data)
            if not self.under_develope:
                cache.set(cache_key, response.data, 60*15)
            return response

        serializer = self.get_serializer(viewable_models)

        return Response(serializer.data)

class TableAppModelViewSet(viewsets.ModelViewSet):

    authentication_classes = [BlacklistJWTAuthentication]
    permission_classes = [IsAuthenticated, CustomModelPermission]

    queryset = AppModels.objects.all()
    serializer_class = serialize_model(AppModels, ['application', 'model'])

    under_develope = settings.DEVELOPMENT_MODE

    @method_decorator(conditional_cache_page(not under_develope, 60*15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class ModifyModelViewSet(viewsets.ModelViewSet):

    authentication_classes = [BlacklistJWTAuthentication]
    permission_classes = [IsAuthenticated, CustomModelPermission]

    def get_model_class(self):
        application = self.request.query_params.get('application', '')
        model_name = self.request.query_params.get('model', '')
        return apps.get_model(application, model_name)

    def get_serializer_class(self):
        ModelClass = self.get_model_class()
        return serialize_model(target_model=ModelClass)

    def get_queryset(self):
        ModelClass = self.get_model_class()
        return ModelClass.objects.all()
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            print(e.detail)  # This will print the errors
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            print(e.detail)  # This will print the errors
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        ModelClass = self.get_model_class()
        instance = ModelClass.objects.get(pk=kwargs['pk'])
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SettingsGetTableContentView(APIView):

    authentication_classes = [BlacklistJWTAuthentication]
    permission_classes = [IsAuthenticated, CustomModelPermission]
    
    def get(self, request, application, model):
        # Initialization
        page = request.GET.get('page', 1)
        version = settings.VERSION
        under_develope = settings.DEVELOPMENT_MODE
        model = apps.get_model(application, model)
        
        # Cache control
        if not under_develope:
            cache_key = f'settings_serialized_model_{model}_{page}:{version}'
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)    # Return cached data if available

        # Perform data transfering
        data = fetch_related_data(request, model)

        if not under_develope:
            cache.set(cache_key, data, 3600) # Cache the data for 1 hour (3600 seconds)
        return Response(data)


@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([AnonRateThrottle])
def index(request):
    # Setting Menus
    app = apps.get_containing_app_config(__name__).name
    nv1index = 0

    # Swiper pictures
    pictures = Pictures.objects.filter(image_settings__app='common', image_settings__name='swiper')
    
    # Countries flag        
    header_contacts = Pictures.objects.filter(image_settings__app='common', image_settings__name='cflag')

    company = CompanyWebsite.objects.get(url=request.META['HTTP_HOST']).company.name 
    
    # All current company menus
    nv1menus = None
    nv2menus = None

    if request.user.is_authenticated:

        try:
            prof_pic = request.user.person.pictures.filter(classification__name="profile").all()
        except:
            prof_pic = None

        # Permissions
        user_permissions = request.user.user_permissions.all()
        group_permissions = Permission.objects.filter(group__user=request.user)
        all_permissions = user_permissions | group_permissions

        try:
            if request.user.is_superuser:
                # User is a superuser, perform the query without checking permissions
                nv1menus = SettingMenus.objects.filter(cat__company__name=company, index=0, parent__isnull=True).order_by('order')
                nv2menus = SettingMenus.objects.filter(cat__company__name=company, index=10, parent__isnull=True).order_by('order')
            else:
                # User is not a superuser, perform the query with permission checks
                nv1menus = SettingMenus.objects.filter(
                    Q(individual_permission__in=all_permissions) | Q(individual_permission__isnull=True),
                    cat__company__name=company, 
                    index=0, 
                    parent__isnull=True
                ).order_by('order')
                nv2menus = SettingMenus.objects.filter(
                    Q(individual_permission__in=all_permissions) | Q(individual_permission__isnull=True),
                    cat__company__name=company, 
                    index=10, 
                    parent__isnull=True
                ).order_by('order')
        except:
            menus = None
    else:
        # Handle the case where the user is not authenticated
        # This could be redirecting them to the login page, for example
        prof_pic = None
        nv2menus = SettingMenus.objects.filter(
            cat__company__name=company, 
            index=10, 
            parent__isnull=True,
            individual_permission__isnull=True
        ).order_by('order')

    return render (request, "common/index.html", {
        "pictures": pictures,
        "prof_pic": prof_pic,
        "header_contacts": header_contacts,
        "nv1menus": nv1menus,
        "nv2menus": nv2menus,
        "company": company,
        "app": app,
        "nv1index": nv1index,
    })


@api_view(['POST', 'GET'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([AnonRateThrottle])
def register(request):
    header_contacts = Pictures.objects.filter(image_settings__app='common', image_settings__name='cflag')
    if request.method == "POST":
        form = Register(request.POST)
        # form valication checking
        if form.is_valid():
            # Attempt to register
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            mobile_number = form.cleaned_data["mob_phone"]
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]
            
            # Ensure password matches confirmation
            if password != confirm_password:
                return render(request, "common/register.html", {
                    "message":"Passwords must match.",
                    "form": form
                })
            # Attempt to create new user
            try:
                default_group = UserRole.objects.get(name='user')
                user = User.objects.create_user(username=username, email=email, password=password)
                user.groups.add(default_group)
                user_profile = UserProfile.objects.create(
                    user=user, 
                    mobile_number=mobile_number,
                )
                # login(request, user)
                # request.session['logged_in_user_id'] = user.id
                delete_expired_tokens()
                blacklist_token(request)
                access_token, refresh_token, access_lifetime = create_new_token(user)
                refresh_lifetime_seconds = settings.SIMPLE_JWT['SLIDING_TOKEN_REFRESH_LIFETIME'].total_seconds()
                access_lifetime_seconds = access_lifetime.total_seconds()
                response = HttpResponseRedirect(reverse('index'))
                response.delete_cookie("access_token")
                response.set_cookie('access_token', access_token,  max_age=access_lifetime_seconds, httponly=True, secure=True, samesite='Lax')
                response.set_cookie('access_token_expiry', access_lifetime_seconds)
                response.set_cookie('refresh_token', refresh_token, max_age=refresh_lifetime_seconds, httponly=True, secure=True, samesite='Lax')
                response.set_cookie('refresh_token_expiry', refresh_lifetime_seconds)
                return response
            except IntegrityError:
                return render(request, "common/register.html", {
                    "message": "Username already taken.",
                    "form": form
                })
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if "Mobile number should be 14 digits." in error:
                        error = "Mobile number should be 14 digits"
                        break
            return render(request, "common/register.html", {
                "form": form,
                "message": error
            })
    else:
        return render (request, "common/register.html", {
            "header_contacts": header_contacts,
            "form":Register()
        })

    logger.error('Something went wrong!')

@api_view(['POST', 'GET'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([AnonRateThrottle])
def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        # form valication checking
        if form.is_valid():
            # Attempt to sign user in
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user=custom_authenticate(username, password)

            # Check if authentication successful
            if user is not None:
                # Handle Token athentication
                delete_expired_tokens()
                blacklist_token(request)
                access_token, refresh_token, access_lifetime = create_new_token(user)
                refresh_lifetime_seconds = settings.SIMPLE_JWT['SLIDING_TOKEN_REFRESH_LIFETIME'].total_seconds()
                access_lifetime_seconds = access_lifetime.total_seconds()

                ip_str = request.META.get('REMOTE_ADDR', '')

                ip_data = extract_ip_data(ip_str)

                user_data = extract_user_agent_data(request)
                user_agent_data = {k: v for k, v in user_data.items() if k != 'device_type'}
                device_type = user_data.get('device_type')

                geo_data = extract_geo_data(ip_str)
                gps_longitude = request.POST.get('gps_longitude') or None
                gps_latitude = request.POST.get('gps_latitude') or None
                location_data = get_location_data(geo_data, gps_longitude, gps_latitude)

                # Create a new Location
                location = None
                if location_data is not None:
                    if any(value for value in location_data.values()):
                        location = Location.objects.create(**location_data)

                # Create a new LoginRecord
                LoginRecord.objects.create(
                    user=user,
                    login_date_time=timezone.now().astimezone(pytz.utc),
                    user_agent_data=user_agent_data,
                    location=location,
                    device_type = device_type,
                    ipv4_address = ip_data['ipv4_address'],
                    ipv6_address = ip_data['ipv6_address'],
                    ip_validation_status = ip_data['ip_validation_status']
                )

                # Ensure session key exists
                request.session.flush()
                session_key = generate_unique_session_key()

                # Create a new UserSession
                UserSession.objects.create(
                    user=user,
                    session_key=session_key,
                    session_data=json.dumps(dict(request.session)),
                    login_time=timezone.now().astimezone(pytz.utc),
                    device_type = device_type,
                    location=location,
                )

                response = redirect('index')
                response.set_cookie('access_token', access_token,  max_age=access_lifetime_seconds, httponly=True, secure=True, samesite='Lax')  # Set token as a cookie
                response.set_cookie('access_token_expiry', access_lifetime_seconds)
                # print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
                # print(access_lifetime_seconds)
                response.set_cookie('refresh_token', refresh_token, max_age=refresh_lifetime_seconds, httponly=True, secure=True, samesite='Lax')
                response.set_cookie('refresh_token_expiry', refresh_lifetime_seconds)
                return response
            else:
                return render(request, "common/login.html", {
                    "form": form,
                    "message": "Invalid athentication!",
                })
        else:
            return render(request, "common/login.html", {
                "form": form,
                "message": "Fill correct data."
            })
    else:
        return render(request, "common/login.html", {
            "form": CustomAuthenticationForm()
        })

# @permission_classes([IsAuthenticated])
# @check_token(redirect_field_name='next', login_url='/login/')
# @authentication_classes([CookieJWTAuthentication])

@check_token(redirect_field_name='next', login_url='/login/')
def logout_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(['POST'])
    blacklist_token(request)
    request.session.flush()
    response = redirect(reverse('index'))
    response.delete_cookie('access_token')
    return response

@login_required(redirect_field_name="next", login_url="login")
@user_passes_test(in_group_admin, redirect_field_name="next", login_url='login')
def settings2(request, item=0):

    # Contact country flags icon
    header_contacts = Pictures.objects.filter(image_settings__app='common', image_settings__name='cflag')

    # All current profile pictures
    try:
        prof_pic = request.user.person.pictures.filter(classification__name="profile").all()
    except:
        prof_pic = None

    # Current company menus index 0
    try:
        company = CompanyWebsite.objects.get(url=request.META['HTTP_HOST']).company.name 
        nv1menus = SettingMenus.objects.all()
        nv1index = 0
    except:
        nv1menus = None

    # Tables which are related to each Menu
    # tables=[apps.get_model(table.application, table.model).objects.all() for table in SettingMenus.objects.get(pk=item).tables.all()]

    tables_data = []
    json_tables_data = []

    for table in SettingMenus.objects.get(pk=item).tables.all():
        application_name = table.application
        
        table_name = table.model
        
        model = apps.get_model(application_name, table_name)

        editable_fields = [field.name for field in model._meta.fields if field.editable]
        
        table_content = model.objects.values(*editable_fields)
        
        table_dict = {
            'ApplicationName': application_name,
            'TableName': table_name,
            'EditableFields': editable_fields,
            'Content': table_content
        }
        json_table_dict = {
            'ApplicationName': application_name,
            'TableName': table_name,
            'EditableFields': editable_fields,
            'Content': list(table_content)
        }
        
        tables_data.append(table_dict)
        json_tables_data.append(json_table_dict)
    tables_json = json.dumps(json_tables_data)

    # Parent and first sub Setting menus
    # settings = [name["name"] for name in list(
    # SettingMenus.objects.filter(parent__name="Settings", role__name__in=request.user.groups.values_list('name', flat=True)).values("name")
    # )]

    # sub_settings = {
    #     setting: [name["name"] for name in list(
    #         SettingMenus.objects.filter(parent__name=setting, role__in=request.user.groups.all()).values("name")
    #     )]
    #     for setting in settings
    # }
    
    return render(request, 'common/settings.html', {
        "header_contacts": header_contacts,
        "apps": get_app_names,
        "prof_pic": prof_pic,
        "nv1menus": nv1menus,
        "company": company,
        "nv1index": nv1index,
        "app": apps.get_containing_app_config(__name__).name,
        "item": item,
        "tables_data": tables_data,
        "tables_json": tables_json,

    })


class GetCountryCodeView(View):
    def get(self, request, *args, **kwargs):
        ip_address = self.get_client_ip(request)
        country_code = None
        if ip_address:
            reader = geoip2.database.Reader(os.path.join(settings.GEOIP_PATH, 'GeoLite2-City.mmdb'))
            try:
                response = reader.city(ip_address)
                country_code = response.country.iso_code
            except geoip2.errors.AddressNotFoundError:
                pass
            reader.close()

        return JsonResponse({'country_code': country_code})

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip








def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'upload_success.html')
    else:
        form = ImageForm()
    return render(request, 'upload_image.html', {'form': form})
