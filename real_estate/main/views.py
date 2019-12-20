# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from datetime import datetime
from django.http import HttpResponse
import requests
import simplejson
import logging
from .models import Apartment

URL = "https://m.land.naver.com/complex/getComplexArticleList"

def real_estate_list(request):

  apartments = Apartment.objects.all().order_by('name')
  return render(request, 'main/real_estate_list.html', { 'apartments' : apartments,} )

def real_estate_detail(request, apt_code ) :

  apartment = get_object_or_404(Apartment, apt_code=apt_code)
  contents = get_real_estate_lists(apt_code)
  time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  return render(request, 'main/real_estate_detail.html', { 'contents' : contents ,
                                                           'counts' : len(contents),
                                                           'apartment' : apartment,
                                                           'time' : time,
                                                           'apt_code' : apt_code})

def real_estate_download( request, apt_code  ) :

  time = datetime.now().strftime('%Y-%m-%d')
  csvfile = "%s_%s.csv" % ( time, apt_code)

  contents = get_real_estate_lists(apt_code)

  import pandas as pd
  results = pd.DataFrame(contents)

  results.index += 1

  results.columns = ['거래유형', '동', '층', '면적', '가격', '집주인인증', '올린일자', '부동산', '중개사', '거래완료' ]
  results.head()

  response = HttpResponse( content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename=%s' % csvfile
  results.to_csv(encoding='utf-8', path_or_buf=response , index=True)

  return response


def get_real_estate_lists(apt_code ) :
  param = {
    'hscpNo': apt_code,
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

    resp = requests.get(URL, params=param, headers=header)

    if resp.status_code != 200:
      logging.error('invalid status : %d' % resp.status_code)
      break

    data = simplejson.loads(resp.content)
    result = data['result']

    if result is None:
      logging.error('No Data')
      break

    for item in result['list']:
      if ( float(item['spc2']) > 84 and float(item['spc2']) < 100  ) :
      #   continue
        append_data = (item['tradTpNm'],  # 거래 유형 (매매, 전세, 월세, 단기임대)
                       item['bildNm'],  # 동
                       item['flrInfo'].split('/')[0],  # 층
                       float(item['spc2']),  # 면적
                       item['prcInfo'],  # 가격
                       '인증' if item['vrfcTpCd'] == 'OWNER' else '', # 집주인 인증
                       item['cfmYmd'],  # 광고 일자
                       item['rltrNm'],  # 부동산
                       item['sameAddrCnt'],  # 부동산 갯수
                       '완료' if item['atclStatCd'] == 'R1' else '', ) # 거래가능여부
        result_list.append(append_data)

    if result['moreDataYn'] == 'N':
      break

  # sorting ( 면적, 광고일자 , 층, 동)
  sorted_list = sorted(result_list, key=lambda result:  (result[3], result[0], result[1], result[2]))
  return sorted_list