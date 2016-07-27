
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^', include([
        url(r'^auth/', include("workon.contrib.auth.urls")),
        url(r'^stripe/', include("workon.contrib.stripe.urls")),
        url(r'^flow/', include("workon.contrib.flow.urls")),
        url(r'^select2/', include("workon.contrib.select2.urls")),
    ], namespace="workon"))
]

include_urls = []

if 'workon.contrib.auth' in settings.INSTALLED_APPS:
    include_urls += [
        url(r'^auth/', include("workon.contrib.auth.urls")),
    ]

if 'workon.contrib.stripe' in settings.INSTALLED_APPS:
    include_urls += [
        url(r'^stripe/', include("workon.contrib.stripe.urls")),
    ]

if 'workon.contrib.flow' in settings.INSTALLED_APPS:
    include_urls += [
        url(r'^flow/', include("workon.contrib.flow.urls")),
    ]

if 'workon.contrib.select2' in settings.INSTALLED_APPS:
    include_urls += [
        url(r'^select2/', include("workon.contrib.select2.urls")),
    ]

# urlpatterns.append(
#     url(r'^', include(include_urls, namespace="workon"))
# )