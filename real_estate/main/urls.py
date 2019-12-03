from django.conf.urls import *

from . import views

urlpatterns = [
  url(r'^$', views.real_estate_list, name='real_estate_list'),
  url(r'^main/(?P<apt_code>\d+)/$', views.real_estate_detail, name='real_estate_detail'),
]