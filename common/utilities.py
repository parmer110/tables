from django.db import models
from django.views.decorators.cache import cache_page

def field_type(field):
    try:
        return type(field).__name__
    except AttributeError:
        return None

def conditional_cache_page(condition, seconds):
    def decorator(func):
        if condition:
            return cache_page(seconds)(func)
        else:
            return func
    return decorator        