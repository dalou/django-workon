# encoding: utf-8
from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r"^activate/(?P<token>\w{10,64})/$", views.Activate.as_view(), name="auth-activate"),
]