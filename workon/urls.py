
from django.conf import settings
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^', include([
        url(r'^emailing/', include("workon.modules.emailing.urls")),
        url(r'^stripe/', include("workon.modules.stripe.urls")),
        url(r'^flow/', include("workon.modules.flow.urls")),
    ], namespace="workon"))
]
