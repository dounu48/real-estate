# -*- coding: utf-8 -*-


import requests
import json
import logging

from smtplib import SMTP
from email import Encoders
from django.utils.encoding import smart_unicode
from datetime import datetime

time = datetime.now()
time = time.strftime('%Y-%m-%d')

url = "https://m.land.naver.com/complex/getComplexArticleList"

SENDER = 'dounu48@hotmail.com'
RECIPIENTS = [ 'leo1891@naver.com', 'dounu48@hotmail.com']
SUBJECTS = '허위매물 관리'
BODY = 'FYI'
SMTP_HOST = 'send.mx.cdnetworks.com'

# 8458 서홍 벽산
# 8438 서홍 한일
# 8437 서홍 한화
# 9014 만현 아이파크5

bldg_code = 8458

def main() :
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

  excel_header = ['거래유형', '동', '층', '면적', '가격', '최저', '최고', '올린일자', '부동산', '올린부동산갯수','거래완료', '비고', '허위']
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
      append_data = ( item['tradTpNm'].encode('utf-8'), # 거래 유형 (매매, 전세, 월세, 단기임대)
                                     item['bildNm'].encode('utf-8'), # 층
                                      (item['flrInfo'].encode('utf-8')).split('/')[0], # 호수
                                     float(item['spc2']), # 면적
                                     item['prcInfo'].encode('utf-8'), # 가격
                                     item['sameAddrMinPrc'].encode('utf-8'), # 최저가격
                                     item['sameAddrMaxPrc'].encode('utf-8'), # 최고가격
                                     item['cfmYmd'].encode('utf-8'), # 광고 일자
                                     item['rltrNm'].encode('utf-8'), # 부동산
                                     item['sameAddrCnt'], # 부동산 갯수
                                     '완료' if item['atclStatCd'].encode('utf-8') == 'R1' else '거래가능',) #거래가능여부
      excel_result.append(append_data)

    if result['moreDataYn'] == 'N' :
      break

  # sorting ( 면적, 거래유형, 층, 동)
  excel_sorted = sorted(excel_result, key=lambda result: ( result[3],result[0], result[1], result[2]))

  import csv
  import codecs

  csvfile = open('./%s_%s.csv' % (time, bldg_code), 'w')
  csvfile.write(codecs.BOM_UTF8)
  writer = csv.writer(csvfile, delimiter=',')
  writer.writerow(excel_header)

  for excel in excel_sorted:
    writer.writerow(excel)

  csvfile.close()
  print("Excel Success")

#  send_email ( SENDER, RECIPIENTS, SUBJECTS, BODY, '%s_%s.csv' % (time, bldg_code))

#  remove_file ('%s_%s.csv' % (time, bldg_code))


def remove_file(filename) :
  import os
  if os.path.exists(filename):
    os.remove(filename)

    print("Remove File Success")

def send_email ( sender, recipients, subject, body, attachment, mime_type = 'plain') :
  if type (recipients ) != list:
    recipients = [recipients]
  else :
    recipients = recipients[:]

  body = smart_unicode(body)
  subject += '_%s' %time
  subject = smart_unicode(subject)

  header_charset = 'ISO-8859-1'

  for body_charset in 'US-ASCII', 'ISO-8859-1', 'UTF-8':
    try:
      body.encode(body_charset)
    except UnicodeError:
      pass
    else:
      break

  from email.mime.text import MIMEText
  from email.mime.base import MIMEBase
  from email.mime.multipart import MIMEMultipart
  from email.header import Header

  msg = MIMEText(body.encode(body_charset), mime_type, body_charset)

  if attachment :
    msg_text = msg
    msg = MIMEMultipart()
    msg.attach(msg_text)

    part = MIMEBase('application', 'octet-stream')
    fp = open('./%s_%s.csv' % (time, bldg_code), "rb")

    part.set_payload(fp.read())
    fp.close()
    Encoders.encode_base64(part)

    part.add_header('Content-Disposition', 'attachment; filename="%s"' % attachment)
    msg.attach(part)

  msg['From'] = sender
  msg['To'] = ', '.join(recipients)
  msg['Subject'] = Header(unicode(subject), header_charset)

  smtp = SMTP(SMTP_HOST)
  smtp.sendmail(sender, recipients, msg.as_string())
  smtp.quit()

  print("Sending Email Success")

if __name__ == '__main__' :
  main()