#!/usr/bin/python
# -*- coding: utf-8 -*-


# 通用文字识别	识别图片中的文字信息 basicGeneralUrl
# 通用文字识别（高精度版）	更高精度地识别图片中的文字信息 basicAccurate
# 通用文字识别（含位置信息版）	识别图片中的文字信息（包含文字区域的坐标信息）
# 通用文字识别（高精度含位置版）	更高精度地识别图片中的文字信息（包含文字区域的坐标信息）
# 通用文字识别（含生僻字版）	识别图片中的文字信息（包含对常见字和生僻字的识别）
# https://cloud.baidu.com/doc/OCR/s/3k3h7yeqa
# https://console.bce.baidu.com/ai/?_=1586591849666#/ai/ocr/report/index

# client = AipOcr(config.APP_ID, config.API_KEY, config.SECRET_KEY)

import requests
import base64
import urllib
import json
import sys

API_KEY = "iRiAOGPF8K8ejm6ybcBSRdIo"
SECRET_KEY = "EQgPHCMlvFNcs3DY5gNg6dwzcEeO5mHB"

def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


def main():
        
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token=" + get_access_token()
    
    base64_string = get_file_content_as_base64(sys.argv[1],True)
    
    payload='image=' + base64_string + '&language_type=JAP&detect_direction=false&vertexes_location=false&paragraph=false&probability=false'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    # print(response.text)
    json_obj = json.loads(response.text)
    for w in json_obj['words_result']:
        print(w['words'])
    

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    main()
