from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),     # This line has changed
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^home$', views.wall),
    url(r'^appointments/(?P<id>\d+)',views.edit),
    url(r'^remove/(?P<id>\d+)', views.remove),
    url(r'^appointments/add/', views.add),
    url(r'^update/(?P<number>\d+)/(?P<id>\d+)$', views.update),
]