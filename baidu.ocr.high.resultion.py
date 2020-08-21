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

# 百度ocr获取图片位置


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 识别文字
image = get_file_content('D:/BaiduNetdiskDownload/2020-08-20 152830.jpg')

# 通用文字识别（高精度版）	更高精度地识别图片中的文字信息 basicAccurate
result = client.basicAccurate(image)
for w in result['words_result']:
    print(w['words'])
