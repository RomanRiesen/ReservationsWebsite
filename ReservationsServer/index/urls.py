from django.conf.urls import url
from django.shortcuts import redirect
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^getdates$', views.getdates),
    #redirect to the sitzreservation module/app/urlSpace
    url(r'^sitzreservation$', lambda r:redirect('/sitzreservation')),
]
