# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from dj_beneficiary import urls as dj_beneficiary_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^accounts/', include('allauth.urls')),
    url(r'^', include(dj_beneficiary_urls)),
    url(r'^', include('base.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
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
