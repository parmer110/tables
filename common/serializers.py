import os
from rest_framework import serializers
from django.apps import apps
from django.db import models
from django.db.models.base import ModelBase
from django.http import QueryDict
from .models import SettingMenus, AppModels
from .utilities import field_type

def serialize_model(target_model='', fields_set='__all__', application='', model=''):
    if target_model:
        target_model = target_model
    else:
        target_model = apps.get_model(application, model)
    class CustomModelSerializer(serializers.ModelSerializer):

        class Meta:
            model = target_model
            fields = fields_set

        def to_representation(self, instance):
            rep = super().to_representation(instance)
            if 'deleted_at' in rep:
                rep.pop('deleted_at')
            if 'password' in rep:
                rep['password'] = '•••'

            for field_name, field in self.fields.items():
                if isinstance(field, serializers.FileField):
                    file = rep.get(field_name)
                    if file:
                        rep[field_name] = os.path.basename(file) if file else None
            return rep
        def to_internal_value(self, data):
            mutable_data = QueryDict('', mutable=True)
            for field_name in data.keys():
                field = self.fields.get(field_name)
                if field and isinstance(field, serializers.ManyRelatedField):
                    values = list(map(int, data[field_name].split(',')))
                    if len(values) == 1:
                        mutable_data.setlist(field_name, [values[0]])
                    else:
                        for value in values:
                            mutable_data.appendlist(field_name, value)
                else:
                    mutable_data.setlist(field_name, data.getlist(field_name))
            return super().to_internal_value(mutable_data)
    return CustomModelSerializer

class ModelInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    app = serializers.CharField()
    editable = serializers.BooleanField()

    def to_representation(self, instance):
        if isinstance(instance, ModelBase):
            model_name = instance.__name__
        else:
            model_name = instance.__class__.__name__

        representation = {
            'name': model_name,
            'app': instance._meta.app_label,
            'editable': self.context.get('editable', False)
        }
        return representation

class FieldInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.CharField()
    editable = serializers.BooleanField()
    nullable = serializers.BooleanField()
    choices = serializers.ListField(child=serializers.DictField(), required=False)
    relationType = serializers.CharField(required=False)
    relatedApp = serializers.CharField(required=False)
    relatedModel = serializers.CharField(required=False)
    

    def to_representation(self, instance):
        field_info = []
        for field in instance._meta.get_fields():
            if field.auto_created and field.name != 'id' or field.name == 'deleted_at':
                continue
            field_dict = {
                'name': field.name,
                'verbose_name': field.verbose_name,
                'type': field_type(field),
                'editable': field.editable,
                'nullable': field.blank,
                'is_file': isinstance(field, models.FileField),
                'choices': [{'value': choice[0], 'label': choice[1]} 
                    for choice in field.choices] 
                    if hasattr(field, 'choices') and field.choices is not None else None,
            }
            # Checking relationships
            if isinstance(field, (models.OneToOneField, models.ForeignKey, models.ManyToManyField)):
                field_dict.update({
                    'relationType': 'one-to-one' if isinstance(field, models.OneToOneField) else \
                    'many-to-one' if isinstance(field, models.ForeignKey) else \
                    'many-to-many',
                    'relatedApp': field.related_model._meta.app_label,
                    'relatedModel': field.related_model._meta.model_name.capitalize(),
                })
            field_info.append(field_dict)

        return {'field': field_info}

class AggregateModelInfoSerializer(serializers.Serializer):
    model_info = ModelInfoSerializer()
    fields_info = FieldInfoSerializer(many=True)

    def to_representation(self, instance):
        field_info = FieldInfoSerializer(instance).data
        field_info = field_info['field']
        representation = {
            'model_info': ModelInfoSerializer(instance).data,
            'field_info': field_info
        }
        return representation
