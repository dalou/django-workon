
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

includes = []

if 'workon.contrib.flow' in settings.INSTALLED_APPS:
    includes.append(url(r'^flow/', include("workon.contrib.flow.urls")))

if 'workon.contrib.select2' in settings.INSTALLED_APPS:
    includes.append(url(r'^select2/', include("workon.contrib.select2.urls")))

if 'workon.contrib.auth' in settings.INSTALLED_APPS:
    includes.append(url(r'^auth/', include("workon.contrib.auth.urls")))

if 'workon.contrib.stripe' in settings.INSTALLED_APPS:
    includes.append(url(r'^stripe/', include("workon.contrib.stripe.urls")))

urlpatterns = [
    url(r'^', include(includes, namespace="workon"))
]
# urlpatterns.append(
#     url(r'^', include(include_urls, namespace="workon"))
# )