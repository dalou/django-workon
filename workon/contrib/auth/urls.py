# encoding: utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^activate/(?P<token>\w{10,64})/$", views.Activate.as_view(), name="auth-activate"),
]