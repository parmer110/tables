from django.conf import settings
from django.apps import apps
from PIL import Image
import os
import uuid
from django.shortcuts import redirect
import importlib
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from datetime import datetime, timedelta
import requests
import geoip2.database
from twilio.rest import Client
from django.conf import settings
# import winreg as reg
import socket
import socks  # Import PySocks
from twilio.http.http_client import TwilioHttpClient
import random
import json
import ipaddress
from django.core.exceptions import ObjectDoesNotExist
from geoip2.errors import AddressNotFoundError
from geoip2.database import Reader as GeoIP2Reader
from django_user_agents.utils import get_user_agent
import logging
import uuid
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import AccessToken

logger = logging.getLogger(__name__)

def get_blacklisted_token_model():
    return apps.get_model('common', 'BlacklistedToken')

def get_user_session_model():
    return apps.get_model('common', 'UserSession')

def get_user_model():
    return apps.get_model('common', 'User')

def generate_verification_code(length=6):
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


def get_system_proxy():
    http_proxy = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
    https_proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
    proxy_dict = {
        'http': None,
        'https': None
    }
    
    if http_proxy:
        proxy_parts = http_proxy.split('://')[-1].split(':')
        if len(proxy_parts) == 2:
            host, port = proxy_parts
            proxy_dict['http'] = f'http://{host}:{port}'
    
    if https_proxy:
        proxy_parts = https_proxy.split('://')[-1].split(':')
        if len(proxy_parts) == 2:
            host, port = proxy_parts
            proxy_dict['https'] = f'https://{host}:{port}'
    
    if proxy_dict['http'] or proxy_dict['https']:
        return proxy_dict
    else:
        return None


def delete_expired_tokens():
    now = timezone.now()
    BlacklistedToken = get_blacklisted_token_model()
    BlacklistedToken.objects.filter(expires_at__lt=now).delete()


def check_blacklist(token):
    BlacklistedToken = get_blacklisted_token_model()
    return BlacklistedToken.objects.filter(token=token).exists()


def check_token_func(request):
    # auth_header = request.headers.get('Authorization')
    # token = auth_header.split(' ')[1] if auth_header and ' ' in auth_header else None
    token = request.COOKIES.get('access_token')

    if token:
        if check_blacklist(token):
            return False
        try:
            UntypedToken(token)
        except (InvalidToken, TokenError):
            return False
    else:
        return False
    return True


def get_token_lifetime(user):
    if user.token_lifetime:
        return user.token_lifetime.lifetime
    group_lifetimes = [group.token_lifetime.lifetime for group in user.groups.all() if group.token_lifetime]
    if group_lifetimes:
        return max(group_lifetimes)
    # مقدار پیش‌فرض اگر تعریف نشده باشد
    return timedelta(minutes=15)


def generate_token(user):
    refresh = RefreshToken.for_user(user)
    # access_lifetime = get_token_lifetime(user)
    # refresh.access_token.set_exp(lifetime=access_lifetime)
    # refresh.set_exp(lifetime=access_lifetime)
    # decoded_token = jwt.decode(str(refresh.access_token), options={"verify_signature": False})
    # expiration_time = datetime.fromtimestamp(decoded_token['exp'])
    access_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
    # print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
    # print(decoded_token)
    return str(refresh.access_token), str(refresh), access_lifetime


def create_new_token(user):
    if not user:
        return False
    for _ in range(10):
        new_token, refresh_token, access_lifetime = generate_token(user)
        if not check_blacklist(new_token):
            return new_token, refresh_token, access_lifetime
    return False, None

def real_token_lifetimes(request):
    """
    Get the expiration time and lifetime of the given JWT token from the request header.
    
    Parameters:
        request (HttpRequest): The incoming HTTP request.
    
    Returns:
        tuple: (expires_at, token_lifetime) where expires_at is the expiration datetime 
               and token_lifetime is the remaining lifetime as a timedelta object.
    """
    try:
        # Assume token is received in header as "Bearer your_access_token"
        received_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        
        # Convert the token string to an AccessToken object
        token = AccessToken(received_token)
        
        # Get the expiration datetime of the token
        expires_at = datetime.fromtimestamp(token.payload['exp'])
        
        # Calculate and return the token's lifetime (as a timedelta)
        token_lifetime = expires_at - datetime.utcnow()
        
        return expires_at, token_lifetime
    
    except (IndexError, KeyError, TypeError, AttributeError):
        return None, None


def blacklist_token(request):
    token = request.COOKIES.get('access_token')
    if token and request.user.is_authenticated:
        try:
            untyped_token = UntypedToken(token)
            expires_at_timestamp = untyped_token['exp']
            # some_datetime = datetime.utcfromtimestamp(expires_at_timestamp)
            some_datetime = timezone.make_aware(datetime.utcfromtimestamp(expires_at_timestamp))
            BlacklistedToken = get_blacklisted_token_model()
            BlacklistedToken.objects.create(token=token, user=request.user, expires_at=some_datetime)
            return True  # توکن با موفقیت به لیست سیاه افزوده شد
        except (TokenError, KeyError):
            pass  # خطایی رخ داده و توکن به لیست سیاه افزوده نشد
    return False  # توکن به لیست سیاه افزوده نشد


def get_location_data(longitude, latitude):
    api_url = f'https://api.opencagedata.com/geocode/v1/json?q={latitude}+{longitude}&key=YOUR_API_KEY'
    response = requests.get(api_url)
    data = response.json()
    if response.status_code == 200:
        location_data = data['results'][0]['components']
        return {
            "name": location_data.get('road', ''),
            "country": location_data.get('country', ''),
            "city": location_data.get('city', ''),
            "region": location_data.get('state', '')
        }
    else:
        raise Exception('Failed to retrieve location data')


def get_geoip_database_info(db_path):
    try:
        with geoip2.database.Reader(db_path) as reader:
            # دریافت اطلاعات متا از دیتابیس
            print(f"IP version: {reader.metadata().ip_version}")
            print(f"Database type: {reader.metadata().database_type}")
            print(f"Build epoch (timestamp): {reader.metadata().build_epoch}")
            print(f"Binary format major version: {reader.metadata().binary_format_major_version}")
            print(f"Binary format minor version: {reader.metadata().binary_format_minor_version}")
    except Exception as e:
        print(f"Error: {e}")


def get_field_value(geo_data, field_name):
    if geo_data is None:
        return None
    try:
        return geo_data[field_name]
    except KeyError:
        print(f'The field {field_name} is not in the geo_data.')
        return None


def send_sms(to, body):
    account_sid = 'AC83af68636faea86c07857252ae4086b7'
    auth_token = '[AuthToken]'
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        from_='+12295979245',
        body=body,
        to=to
    )
    
    return message.sid
# sms_sid = send_sms('+989390432897', 'سلام سمیرا جون.\nچه‌طوری، چیکار می‌کنی؟')

account_sid = 'AC83af68636faea86c07857252ae4086b7'
auth_token = '724d28f7951522d19d38edf11feeee02'
client = Client(account_sid, auth_token)

def send_verification_code(phone_number):
    verification_code = generate_verification_code()
    message = client.messages.create(
        body=f'Your verification code is: {verification_code}',
        from_='+12295979245',  # شماره تلفن Twilio خود را وارد کنید
        to=phone_number
    )
    return verification_code

def verify_phone_number(user_input, verification_code):
    return user_input == verification_code

def extract_ip_data(ip_str):
    ipv4_address = ''
    ipv6_address = ''
    ip_validation_status = ''
    
    try:
        ip_obj = ipaddress.ip_address(ip_str)
        if ip_obj.version == 4:
            ipv4_address = ip_str
        elif ip_obj.version == 6:
            ipv6_address = ip_str
    except ValueError:
        ip_validation_status = 'Invalid IP: Could not determine IP version'
    
    ip_data = {
        'ipv4_address': ipv4_address,
        'ipv6_address': ipv6_address,
        'ip_validation_status': ip_validation_status
    }
    return ip_data

def extract_user_agent_data(request):
    user_agent = get_user_agent(request)
    data = {
        "browser": user_agent.browser.family,
        "browser_version": user_agent.browser.version_string,
        "os": user_agent.os.family,
        "os_version": user_agent.os.version_string,
        "device": user_agent.device.family,
        "device_type": "Desktop" if user_agent.is_pc else "Mobile" if user_agent.is_mobile else "Tablet"
    }
    return data

def extract_geo_data(ip_str):
    db_path = os.path.join(settings.GEOIP_PATH, 'GeoLite2-City.mmdb')
    geo = GeoIP2Reader(db_path)
    try:
        return geo.city(ip_str)
    except AddressNotFoundError:
        logger.error(f'The address {ip_str} is not in the database.')
        return None

def get_location_data(geo_data, gps_longitude, gps_latitude):
    if not geo_data:
        return None
    return {
        'name': f'{geo_data.city.name}, {geo_data.subdivisions.most_specific.name}, {geo_data.country.name}',
        'country': geo_data.country.name,
        'region': geo_data.subdivisions.most_specific.name,
        'city': geo_data.city.name,
        'longitude': geo_data.location.longitude,
        'latitude': geo_data.location.latitude,
        'gps_longitude': gps_longitude,
        'gps_latitude': gps_latitude,
    }

def generate_unique_session_key(max_retries=10):
    for _ in range(max_retries):
        session_key = uuid.uuid4().hex  # Generate a unique key
        if not get_user_session_model().objects.filter(session_key=session_key).exists():
            return session_key  # If the key is unique, return it
    raise ValueError(f"Failed to generate a unique session key after {max_retries} attempts.")

def custom_authenticate(username, password):
    try:
        user = get_user_model().objects.get(username=username)
        if check_password(password, user.password):
            return user
    except get_user_model().DoesNotExist:
        pass
    return None








    

    
get_app_names = []
app_configs = apps.get_app_configs()

for app_config in app_configs:
    app_name = app_config.name.split('.')[-1]
    get_app_names.append((app_name, app_name))

# get_app_models_choices= []
# app_configs = apps.get_app_configs()
# for app_config in app_configs:
#     app_name = app_config.name
#     app_models = app_config.get_models()
#     for model in app_models:
#         get_app_models_choices.append((f"{app_name}.{model.__name__}", model.__name__))


def get_max_image_size(settings):
    return settings.max_image_size_width, settings.max_image_size_height

def get_allowed_image_formats(settings):
    return settings.allowed_image_formats

def generate_unique_image_filename(image):
    _, ext = os.path.splitext(image.name)
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    return unique_filename

def process_image(image, settings):
    max_image_size = get_max_image_size(settings)
    allowed_formats = get_allowed_image_formats(settings)

    if image:
        img = Image.open(image)
        img.thumbnail(max_image_size)
        img_format = img.format.lower()
        if img_format not in allowed_formats:
            raise ValueError("Image format not allowed")
        
        return img
    return None


def load_specialty_module(module_name):
    module = __import__(module_name)
    components = module_name.split('.')
    for comp in components[1:]:
        module = getattr(module, comp)
    return module


def has_group(group_name):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                # اقدامات مورد نظر در صورت عدم دسترسی
                return redirect('access_denied_page')  # مثال: انتقال به صفحه عدم دسترسی
        return wrapper
    return decorator

def get_current_app_name():
    return apps.get_containing_app_config(__name__).name

# def get_app_models_choices():
#     app_configs = apps.get_app_configs()
#     choices = []
#     for app_config in app_configs:
#         app_name = app_config.name
#         app_models = app_config.get_models()
#         for model in app_models:
#             choices.append((f"{app_name}.{model.__name__}", model.__name__))
#     return tuple(choices)


def get_app_models_choices_pure():
    app_configs = apps.get_app_configs()
    choices = []
    for app_config in app_configs:
        app_name = app_config.name
        app_models = app_config.get_models()
        for model in app_models:
            choices.append((model.__name__, model.__name__))
    return choices


def get_sub_app_models(app_name):
    app_models = apps.get_app_config(app_name).get_models()
    model_names = [model.__name__ for model in app_models]
    return model_names