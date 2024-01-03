from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from .models import BlacklistedToken
from rest_framework import exceptions

class BlacklistJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            token = super().authenticate(request)
            if token is None:
                raise exceptions.AuthenticationFailed('No token provided!')
            if BlacklistedToken.objects.filter(token=token).exists():
                raise exceptions.AuthenticationFailed('Loged Out!')
            return token
        except:
            raise exceptions.AuthenticationFailed('Authentication credentials have expired!')
