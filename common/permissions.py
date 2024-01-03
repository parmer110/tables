from rest_framework import permissions
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured

class CustomModelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            try:
                model = view.queryset.model
            except AttributeError: 
                model = view.get_model_class()
        except AttributeError:
            application = view.kwargs.get('application')
            model_name = view.kwargs.get('model')
            model = apps.get_model(application, model_name)
        
        permission_map = {
            'GET': f'{model._meta.app_label}.view_{model._meta.model_name}',
            'POST': f'{model._meta.app_label}.add_{model._meta.model_name}',
            'PUT': f'{model._meta.app_label}.change_{model._meta.model_name}',
            'PATCH': f'{model._meta.app_label}.change_{model._meta.model_name}',
            'DELETE': f'{model._meta.app_label}.delete_{model._meta.model_name}',
        }
        permission = permission_map.get(request.method)
        return request.user.has_perm(permission)