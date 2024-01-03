from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'table_app_model', views.TableAppModelViewSet, basename='table-title')
router.register(r'tables_index_from_menus_record', views.SettingMenusTablesIndexViewSet, basename='tables_ind')
router.register(r'table_update', views.ModifyModelViewSet, basename='table_upd')

urlpatterns = [
    path("", views.index, name="index"),
    path('upload/', views.upload_image, name='upload_image'),
    path('register/', views.register, name='register'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("settings/<int:item>", views.settings2, name="settings2"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('country-code/', views.GetCountryCodeView.as_view(), name='get-country-code'),

    path("set_session/<str:key>/<str:value>/", views.set_session, name="set_session"),
    path("get_session/<str:key>", views.get_session, name="get_session"),
    path("serialized_table/<str:application>/<str:model>", views.SettingsGetTableContentView.as_view(), name="get_table"),
    path('', include(router.urls)), 
]
# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
