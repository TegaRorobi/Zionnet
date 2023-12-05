"""
URL configuration for zionnet project.
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Zionnet Project API",
        default_version="v1",
        description="API Documentation for the Zionnet API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@zionnet.ca"),
        license=openapi.License(name="Zionnet License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # DRF-Swagger URLs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # URLconfs
    path('accounts/', include('Accounts.urls')),
    path('BusinessDirectory/', include('BusinessDirectory.urls')),
    path('accounts/', include('Accounts.urls')),
    path('api/', include('BusinessDirectory.urls')),
    path('api/', include('MarketPlace.urls')),

    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
