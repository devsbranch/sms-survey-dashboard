# -*- coding: utf-8 -*-
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from dj_beneficiary import urls as dj_beneficiary_urls

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
]

try:
    from core.urls import urlpatterns as core_urlpatterns
    urlpatterns += core_urlpatterns
except ImportError:
    pass

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
