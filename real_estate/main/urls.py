from django.conf.urls import *

from . import views

urlpatterns = [
  url(r'^', views.real_estate_list, name='real_estate_list')
]