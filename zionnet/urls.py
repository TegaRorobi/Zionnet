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
from drf_yasg.generators import OpenAPISchemaGenerator

version = "v1"



class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ['https', 'http'] if settings.DEBUG else ['https']
        return schema

schema_view = get_schema_view(
    openapi.Info(
        title="Zionnet Project API",
        default_version=version,
        description="API Documentation for the Zionnet API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@zionnet.ca"),
        license=openapi.License(name="Zionnet License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=CustomSchemaGenerator
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # DRF-Swagger URLs
    path(f'api/{version}/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(f'api/{version}/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(f'api/{version}/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # URLconfs
    path(f'accounts/{version}/', include('Accounts.urls')),
    path(f'api/{version}/', include('BusinessDirectory.urls')),
    path(f'api/{version}/', include('MarketPlace.urls')),
    path(f'api/{version}/', include('JobPosting.urls')),

    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
