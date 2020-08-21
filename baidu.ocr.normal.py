#!/usr/bin/python
# -*- coding: utf-8 -*-

from aip import AipOcr
import config

# 通用文字识别	识别图片中的文字信息 basicGeneralUrl
# 通用文字识别（高精度版）	更高精度地识别图片中的文字信息 basicAccurate
# 通用文字识别（含位置信息版）	识别图片中的文字信息（包含文字区域的坐标信息）
# 通用文字识别（高精度含位置版）	更高精度地识别图片中的文字信息（包含文字区域的坐标信息）
# 通用文字识别（含生僻字版）	识别图片中的文字信息（包含对常见字和生僻字的识别）
# https://cloud.baidu.com/doc/OCR/s/3k3h7yeqa
# https://console.bce.baidu.com/ai/?_=1586591849666#/ai/ocr/report/index

client = AipOcr(config.APP_ID, config.API_KEY, config.SECRET_KEY)

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content('C:/Users/wisdom/Downloads/a30.png');

""" 调用通用文字识别, 图片参数为本地图片 """
result = client.basicGeneral(image);
#print(result)
for w in result['words_result']:
    print(w['words'])