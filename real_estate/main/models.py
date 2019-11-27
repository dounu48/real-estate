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
  state_code = models.SmallIntegerField(unique=True)
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name

  def __unicode__(self):
    return self.name

class RegionCode ( models.Model) :
  region_code = models.SmallIntegerField()
  state_code = models.ManyToManyField(StateCode)
  name = models.CharField(max_length=200)

  def __str__(self):
    return self.name

  def __unicode__(self):
    return self.name


class Apartment ( models.Model) :
  name = models.CharField(max_length=255)
  region_code = models.ManyToManyField(RegionCode)
  apt_code = models.SmallIntegerField()

  def __str__(self):
    return self.name


  def __unicode__(self):
    return self.name


# class RealEstate (models.Model) :
# 거래 유형 (매매, 전세, 월세, 단기임대)
# 동
# 층
# 면적
# 가격
# 최저가격
# 최고가격
