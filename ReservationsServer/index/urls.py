from django.conf.urls import url
from django.shortcuts import redirect
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^getdates$', views.getdates),
    url(r'^dateselection$', views.dateselection),
    #redirect to the sitzreservation module/app/urlSpace
    url(r'^sitzverteilung$', lambda r:redirect('/sitzreservation/sitzverteilung')),
    url(r'.*', lambda r:redirect('/sitzreservation')),
]
