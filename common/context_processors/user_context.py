# context_processors/user_context.py
from django.conf import settings
from common.models import User
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
import logging
from django.core.cache import cache

def user_context(request):
    user = request.user or None
    token = request.COOKIES.get('access_token')  # Assume the token is stored in cookies
    # auth_header = request.headers.get('Authorization')
    # token = auth_header.split(' ')[1] if auth_header and ' ' in auth_header else None
    
    if token:
        try:
            untyped_token = UntypedToken(token)
            user_id = untyped_token['user_id']
            # Use user_id instead of the token to create a cache key
            under_develope = settings.DEVELOPMENT_MODE
            cache_key = f'user:{user_id}'
            if not under_develope:
                cached_user = cache.get(cache_key)
                if cached_user:
                    return {'user': cached_user}
            user = User.objects.filter(id=user_id).first()
            if user:
                # Store user in cache for future requests using the user_id-based cache key
                cache.set(cache_key, user, timeout=3600)  # cache for 1 hour
        except TokenError as e:
            logging.error(f"Invalid Token error: {e}")
    return {'user': user}