# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from drf_yasg2 import openapi
from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from dj_beneficiary import urls as dj_beneficiary_urls

schema_view = get_schema_view(
   openapi.Info(
      title="THINK2044 PPCR - TRALARD API",
      default_version='v1',
      description="PPCR - TRALARD Program Data sharing API.",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

api_docs_urlpatterns = [
    path('api/v1/ppcr-tralard/', include("tralard.api_router")),
    path('accounts/', include('rest_registration.api.urls')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


urlpatterns = [

    # must be before admin entry
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include("authentication.urls")), # Auth routes - login / register
    path('', include('base.urls')),
    path('', include('ppcr.urls', namespace='ppcr')),
    path('', include('tralard.urls', namespace='tralard')),
    path('', include(dj_beneficiary_urls)),
    path('reports_builder/', include('report_builder.urls')),
    path('tinymce/', include('tinymce.urls')),
] + api_docs_urlpatterns

try:
    from core.urls import urlpatterns as core_urlpatterns
    urlpatterns += core_urlpatterns
except ImportError:
    pass

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
