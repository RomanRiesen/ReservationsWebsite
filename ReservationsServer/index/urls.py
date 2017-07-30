from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Index, name='index'),
    url(r'^(?P<get_dates>[0-9]+)/$', views.getdates),
]
