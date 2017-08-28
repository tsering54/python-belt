from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.add),
    url(r'^create$', views.create),
    url(r'^travels/destination/(?P<dest_id>\d+)$', views.show),
    url(r'^join/(?P<dest_id>\d+)$', views.join),
    url(r'^logout$', views.logout),


]
