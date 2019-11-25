# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
import requests
import logging
import simplejson
import logging
import pprint

url = "https://m.land.naver.com/complex/getComplexArticleList"

def real_estate_list(request):
  result = get_real_estate_lists(8458)

  contents = []
  for ret in result:
    contents.append(list(ret))

  return render(request, 'main/real_estate_list.html', { 'contents' : contents } )


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

  excel_header = ['거래유형', '동', '층', '면적', '가격', '최저', '최고', '올린일자', '부동산', '올린부동산갯수', '거래완료', '비고', '허위']
  excel_result = []

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
                     item['sameAddrMinPrc'],  # 최저가격
                     item['sameAddrMaxPrc'],  # 최고가격
                     item['cfmYmd'],  # 광고 일자
                     item['rltrNm'],  # 부동산
                     item['sameAddrCnt'],  # 부동산 갯수
                     '완료' if item['atclStatCd'] == 'R1' else '거래가능',)  # 거래가능여부
      excel_result.append(append_data)

    if result['moreDataYn'] == 'N':
      break

  # sorting ( 면적, 거래유형, 층, 동)
  excel_sorted = sorted(excel_result, key=lambda result: (result[3], result[0], result[1], result[2]))
  return excel_sorted