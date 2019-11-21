# -*- coding: utf-8 -*-


import requests
import json
import logging

url = "https://m.land.naver.com/complex/getComplexArticleList"


# 8458 서홍 벽산
# 8438 서홍 한일
# 8437 서홍 한화
# 9014 만현 아이파크5

bldg_code = 9014

param = {
  'hscpNo' : bldg_code,
  'tradTpCd' : 'A1:B1:B2:B3', #A1 매매, B1 전세, B2 월세, B3 단기임대
   'showR0': 'N',
  'articleListYN' : 'Y',
  'order' : 'date_' #point 랭킹순, prc 가격순, 최신순 date, 면적순 spc
}

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.220 Whale/1.3.51.7 Safari/537.36',
    'Referer': 'https://m.land.naver.com/'

}

logging.basicConfig(level= logging.INFO)
page = 0

excel_header = ['type', 'building', '호수', '면적', 'price', 'min_price', 'max_price', 'date', 'realtor', 'cnt_realtors','비고', '허위']
excel_result = []

while True :
  page += 1
  param['page'] = page

  resp = requests.get(url, params=param, headers=header)

  if resp.status_code != 200 :
    logging.error('invalid status : %d' % resp.status_code)
    break

  data = json.loads(resp.text)
  result = data['result']
  if result is None :
    logging.error ('No Data')
    break

  for item in result['list'] :
    # if float(item['spc2']) < 80 or float(item['spc2'] > 85) :
    #   continue
    append_data = ( item['tradTpNm'].encode('utf-8'),
                                   item['bildNm'].encode('utf-8'),
                                   item['flrInfo'].encode('utf-8'),
                                   item['spc2'],
                                   item['prcInfo'].encode('utf-8'),
                                   item['sameAddrMinPrc'].encode('utf-8'),
                                   item['sameAddrMaxPrc'].encode('utf-8'),
                                   item['cfmYmd'].encode('utf-8'),
                                   item['rltrNm'].encode('utf-8'),
                                   item['sameAddrCnt'] )
    excel_result.append(append_data)

  if result['moreDataYn'] == 'N' :
    break

excel_sorted = sorted(excel_result, key=lambda result: ( result[3],result[0], result[1], result[2]))


import csv
import codecs
from datetime import datetime

time = datetime.now()
time = time.strftime('%Y-%m-%d')
print (time)

csvfile = open('./%s_%s.csv' % (time, bldg_code), 'w')
csvfile.write(codecs.BOM_UTF8)
writer = csv.writer(csvfile, delimiter=',')
writer.writerow(excel_header)

for excel in excel_sorted:
  writer.writerow(excel)

csvfile.close()
print("Success")

