
from django.conf import settings
from django.conf.urls import include, url, patterns
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
