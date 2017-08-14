from django.conf.urls import url
from django.shortcuts import redirect
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^getdates$', views.getdates),
    url(r'^dateselection$', views.dateselection),
    #FIXME remove this when front end changes to /sitzreservation as it shoudl.
    #redirect to the sitzreservation module/app/urlSpace
    url(r'^sitzverteilung$', views.sitzverteilung),
    url(r'^sitzreservation$', views.sitzreservation),
    url(r'^getreservation/(?P<date>[\S\s]{0,50})/', views.getreservation),
    url(r'^reserved$', views.reserved),
]
