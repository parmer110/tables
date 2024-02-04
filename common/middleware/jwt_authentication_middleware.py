from django.core.exceptions import PermissionDenied
from common.models import User
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import AccessToken
from common.utils.tools import check_blacklist
from rest_framework.test import force_authenticate
from django.urls import reverse
import logging
from common.utils.tools import check_token_func

logger = logging.getLogger(__name__)

class JWTAuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        token = request.COOKIES.get('access_token')
        if check_token_func(request):
            try:
                valid_token = AccessToken(token)
                user_model = User
                try:
                    request.user = User.objects.get(id=valid_token['user_id'])
                    force_authenticate(request, request.user)
                except user_model.DoesNotExist:
                    return JsonResponse({'error': 'User does not exist'}, status=401)
            except TokenError as e:
                logger.error(f"Token error: {e}")
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'
            
