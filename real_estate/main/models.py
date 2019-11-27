# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


# Create your models here.

# 1 서울특별시
# 2 경기도
# 3 인천광역시
# 4 부산광역시
# 5 대전광역시
# 6 대구광역시
# 7 울산광역시
# 8 세종시
# 9 광주광역시
# 10 강원도
# 11 충청북도
# 12 충청남도
# 13 경상북도
# 14 경상남도
# 15 전라북도
# 16 전라남도
# 17 제주도

class StateCode ( models.Model) :
  state_id = models.IntegerField(default=0)
  name = models.CharField(max_length=100)

  def __str__(self):
    return "%s %s" % ( self.state_id, self.name )

  def __unicode__(self):
    return self.name

class RegionCode ( models.Model) :
  region_id = models.IntegerField(default=0)
  state = models.ForeignKey(StateCode)
  name = models.CharField(max_length=200)

  def __str__(self):
    return "%s %s" % ( self.region_id, self.name )

  def __unicode__(self):
    return self.name

class Apartment ( models.Model) :
  apt_id = models.IntegerField(default=0)
  region = models.ForeignKey(RegionCode)
  name = models.CharField(max_length=255)
  apt_code = models.IntegerField(null=False, default=0)

  def __str__(self):
    return self.name

  def __unicode__(self):
    return self.name
