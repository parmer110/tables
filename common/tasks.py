from django.shortcuts import get_object_or_404
from .serializers import serialize_model, AggregateModelInfoSerializer
from django.apps import apps
from rest_framework.response import Response
from .models import SettingMenus
from .pagination import StandardResultsSetPagination


def fetch_related_data(request, model):

    model_info_dict = {}

    if 'deleted_at' in [field.name for field in model._meta.get_fields()]:
        model_instance = model.objects.filter(deleted_at__isnull=True).first()
        model_instances = model.objects.filter(deleted_at__isnull=True).all()
    else:
        model_instance = model.objects.first()
        model_instances = model.objects.all()

    
    if model_instance:
        serializer = AggregateModelInfoSerializer(model_instance)
    else:
        serializer = AggregateModelInfoSerializer(model)

    model_metadata = serializer.data

    # Pagination using customized StandardResultsSetPagination Paginatior
    page_size = request.GET.get('page_size', 10)
    paginator = StandardResultsSetPagination(page_size=page_size)
    # model_instances = model.objects.all().order_by('id')
    model_instances = model_instances.order_by('id')
    model_instances_paginated_field = paginator.paginate_queryset(model_instances, request)

    # Get model info using the CustomModelSerializer
    serializer = serialize_model(model)

    if model_instances_paginated_field:
        serializer = serializer(model_instances_paginated_field, many=True)
        response = paginator.get_paginated_response(serializer.data)
    else:
        serializer = serializer(model_instances, many=True)
        response = Response(serializer.data)

    model_metadata['model_instances'] = response.data
    return model_metadata
