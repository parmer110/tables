from django.http import HttpResponseForbidden, HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from common.utils.tools import check_blacklist
from functools import wraps
from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from common.models import User, BlacklistedToken


def group_required(group_name):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                # کاربر مجاز نیست، می‌توانید اینجا به دلخواه خطا یا redirect انجام دهید
                return HttpResponse("Access Denied")

        return wrapper

    return decorator

def check_blacklisted_token(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get('access_token')
        if token and check_blacklist(token):
            response = HttpResponseForbidden('BL! Retry please.')
            response.delete_cookie('access_token')  
            return response
        return view_func(request, *args, **kwargs)
    return _wrapped_view


class CookieJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        # auth_header = request.headers.get('Authorization')
        # token = auth_header.split(' ')[1] if auth_header and ' ' in auth_header else None
        if not token:
            return None  # Authentication failed as token is not provided

        try:
            untyped_token = UntypedToken(token)
        except TokenError as e:
            raise AuthenticationFailed(str(e))

        try:
            user_id = untyped_token['user_id']
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

        return (user, None)  # Authentication successful


def check_token(redirect_field_name='next', login_url=None):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            try:
                token = request.COOKIES.get('access_token')  # فرض می‌کنیم توکن در کوکی‌ها ذخیره شده است
            except:
                if login_url:
                    redirect_url = login_url
                else:
                    redirect_url = '/login/'
                return redirect(redirect_url)
            # auth_header = request.headers.get('Authorization')
            # token = auth_header.split(' ')[1] if auth_header and ' ' in auth_header else None
            if token:
                if check_blacklist(token):
                    # اگر توکن در بلک‌لیست باشد
                    if login_url:
                        redirect_url = login_url
                    else:
                        redirect_url = '/login/'
                    redirect_url += f'?{redirect_field_name}={request.path}'
                    return redirect(redirect_url)
                try:
                    UntypedToken(token)
                except (InvalidToken, TokenError):
                    # اگر توکن اعتبار نداشته باشد
                    if login_url:
                        redirect_url = login_url
                    else:
                        redirect_url = '/login/'
                    redirect_url += f'?{redirect_field_name}={request.path}'
                    return redirect(redirect_url)
            else:
                # اگر توکن وجود نداشته باشد
                if login_url:
                    redirect_url = login_url
                else:
                    redirect_url = '/login/'
                redirect_url += f'?{redirect_field_name}={request.path}'
                return redirect(redirect_url)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def check_token_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # تشخیص نوع اولین آرگومان
        if isinstance(args[0], HttpRequest):
            request = args[0]
        else:
            request = args[1]

        token = request.COOKIES.get('access_token')
        if token:
            if check_blacklist(token):
                return Response({'error': 'Token is blacklisted'}, status=401)
            try:
                UntypedToken(token)
            except (InvalidToken, TokenError) as e:
                return Response({'error': str(e)}, status=401)
        else:
            return Response({'error': 'Token is missing'}, status=401)

        return func(*args, **kwargs)

    return wrapper
