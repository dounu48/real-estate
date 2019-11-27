# -*- coding: utf-8 -*-

from django.shortcuts import render
from datetime import datetime

# Create your views here.

from django.shortcuts import render
import requests
import logging
import simplejson
import logging

from .models import Apartment

url = "https://m.land.naver.com/complex/getComplexArticleList"

def real_estate_list(request):
  # get real estate lists from NAVER
  result = get_real_estate_lists(8458)

  apartments = get_apartment_lists()

  # tuple to list
  contents = []
  for ret in result:
    contents.append(list(ret))

  time = datetime.now()
  time.strftime("%Y-%m-%d %H:%M:%S")

  return render(request, 'main/real_estate_list.html', { 'contents' : contents ,
                                                         'time' : time,
                                                         'counts' : len(contents),
                                                         'apartments' : apartments,
                                                         } )
def get_apartment_lists() :
  apartments = Apartment.objects.filter()
  return apartments


def get_real_estate_lists(bldg_code) :
  param = {
    'hscpNo': bldg_code,
    'tradTpCd': 'A1:B1:B2:B3',  # A1 매매, B1 전세, B2 월세, B3 단기임대
    'showR0': 'N',
    'articleListYN': 'Y',
    'order': 'date_'  # point 랭킹순, prc 가격순, 최신순 date, 면적순 spc
  }

  header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.220 Whale/1.3.51.7 Safari/537.36',
    'Referer': 'https://m.land.naver.com/'

  }

  logging.basicConfig(level=logging.INFO)
  page = 0

  result_list = []

  while True:
    page += 1
    param['page'] = page

    resp = requests.get(url, params=param, headers=header)

    if resp.status_code != 200:
      logging.error('invalid status : %d' % resp.status_code)
      break

    data = simplejson.loads(resp.content)
    result = data['result']

    if result is None:
      logging.error('No Data')
      break

    for item in result['list']:
      # if float(item['spc2']) < 80 or float(item['spc2'] > 85) :
      #   continue
      append_data = (item['tradTpNm'],  # 거래 유형 (매매, 전세, 월세, 단기임대)
                     item['bildNm'],  # 동
                     item['flrInfo'].split('/')[0],  # 층
                     float(item['spc2']),  # 면적
                     item['prcInfo'],  # 가격
                     '집주인 인증' if item['vrfcTpCd'] == 'OWNER' else '', # 집주인 인증
                     item['cfmYmd'],  # 광고 일자
                     item['rltrNm'],  # 부동산
                     item['sameAddrCnt'],  # 부동산 갯수
                     '완료' if item['atclStatCd'] == 'R1' else '',)  # 거래가능여부
      result_list.append(append_data)

    if result['moreDataYn'] == 'N':
      break

  # sorting ( 면적, 거래유형, 층, 동)
  sorted_list = sorted(result_list, key=lambda result: (result[3], result[0], result[1], result[2]))
  return sorted_list