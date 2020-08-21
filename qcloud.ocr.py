#!/usr/bin/env python
# -*- coding: utf-8 -*-
from qcloud_image import Client, CIFiles
import time

appid = '1253872891'
secret_id = 'AKIDtakiU04I6e0B6pmYYIm0yjESM6dxsrPh'
secret_key = 'A7oFajdR1NXQ2RhiSwEG2buxjFhEagBT'
bucket = 'ocr1'

client = Client(appid, secret_id, secret_key, bucket)
client.use_http()
client.set_timeout(30)

time1=time.time()

# 这里支持传入多个需要鉴别的本地图片地址
print(client.porn_detect(CIFiles(['C:/Users/wisdom/Downloads/chongding.jpg',])))

#print(client.generalocr(CIFiles(['C:/Users/wisdom/Downloads/chongding.jpg',])))

time2=time.time()

print(time2-time1)