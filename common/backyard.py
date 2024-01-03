#  Views.py↓

# class TableInfoViewSet(viewsets.ReadOnlyModelViewSet):

#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     queryset = SettingMenus.objects.all()
#     serializer_class = SettingMenusSerializer

#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#     # serializer_class = BaseSerializer



# class TablesViewSet(viewsets.ReadOnlyModelViewSet):

#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     queryset = SettingMenus.objects.all()
#     serializer_class = SettingMenusSerializer    


# class TableInfoViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = SettingMenus.objects.all().prefetch_related('tables')
#     pagination_class = StandardResultsSetPagination

#     def fill(self, instance):
#         related_model_classes = self.get_related_model_classes(instance)
#         serializers = {model_class: self.get_serializer_class(model_class) for model_class in related_model_classes}
#         return related_model_classes, serializers

#     def get_related_model_classes(self, setting_menu):
#         related_model_classes = []
#         for app_model in setting_menu.tables.all():
#             model_class = apps.get_model(app_model.application, app_model.model)
#             related_model_classes.append(model_class)
#         return related_model_classes

#     def get_serializer_class(self, model_class):
#         class DynamicSerializer(drf_serializers.ModelSerializer):
#             class Meta:
#                 model = model_class
#                 fields = '__all__'
#         return DynamicSerializer

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         related_model_classes, serializers = self.fill(instance)
#         data = fetch_related_data(instance.pk)  # Use the fetch_related_data function to get the data

#         model_list = list(data['models'].values())
#         page = self.paginate_queryset(model_list)  # Use DRF's pagination

#         if page is not None:
#             return self.get_paginated_response({
#                 'results': page,
#                 'count': self.paginator.page.paginator.count,
#             })

        # If pagination is not used or needed
        # return Response({'results': data['models']})
                

# @authentication_classes([BlacklistJWTAuthentication])
# @permission_classes([IsAuthenticated])
# @check_token(redirect_field_name='next', login_url='login/')
# @authentication_classes([CookieJWTAuthentication])

# permission_classes = [IsAuthenticated]
# authentication_classes = [JWTAuthentication]


#  Views.py↑