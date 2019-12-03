# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import  Apartment

# Register your models here.

#admin id and password
# admin/ qwer1234

admin.site.register(Apartment)