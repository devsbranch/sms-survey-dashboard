# -*- coding: utf-8 -*-
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from dj_beneficiary import urls as dj_beneficiary_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(dj_beneficiary_urls)),
    path('', include("authentication.urls")), # Auth routes - login / register
    path('', include('ppcr.urls', namespace='ppcr')),
    path('', include('tralard.urls', namespace='tralard')),
    path('', include('base.urls')),
]

admin.site.site_header = "PPCR Administration"                   
admin.site.site_title = "PPCR Administration" 
admin.site.index_title = "Project Implementation and Beneficiary Tracking."                 

try:
    from core.urls import urlpatterns as core_urlpatterns
    urlpatterns += core_urlpatterns
except ImportError:
    pass

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
