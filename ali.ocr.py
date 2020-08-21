# -*- coding: utf-8 -*-

import sys
import os
import base64
import json

from urllib.parse import urlparse
import urllib.request
import base64

ENCODING = 'utf-8'


def get_img_base64(img_file):
    with open(img_file, 'rb') as infile:
        s = infile.read()
        return base64.b64encode(s).decode(ENCODING)


def predict(url, appcode, img_base64, kv_configure):
    param = {}
    param['image'] = img_base64
    if kv_configure is not None:
        param['configure'] = json.dumps(kv_configure)
    body = json.dumps(param)
    data = bytes(body, "utf-8")

    headers = {'Authorization': 'APPCODE %s' % appcode}
    request = urllib.request.Request(url=url, headers=headers, data=data)
    try:
        response = urllib.request.urlopen(request, timeout=10)
        return response.code, response.headers, response.read()
    except urllib.request.HTTPError as e:
        return e.code, e.headers, e.read()


def demo():
    appcode = '57c35bf8cacb40419e85da6ac95eb0ed'
    #url = 'http://dm-51.data.aliyun.com/rest/160601/ocr/ocr_idcard.json'
    url = 'https://tysbgpu.market.alicloudapi.com/api/predict/ocr_general'
    #img_file = '图片文件路径/图片url'
    #img_file = 'http://139.9.90.110/a.png'
    img_file = 'D:/BaiduNetdiskDownload/2020-08-20 152830.jpg'
    configure = {"min_size": 16,  # 图片中文字的最小高度，单位像素
                 "output_prob": True,  # 是否输出文字框的概率
                 "output_keypoints": False,  # 是否输出文字框角点
                 "skip_detection": False,  # 是否跳过文字检测步骤直接进行文字识别
                 "without_predicting_direction": False  # 是否关闭文字行方向预测
                 }
    # 如果没有configure字段，configure设为None
    #configure = None

    img_base64data = get_img_base64(img_file)
    stat, header, content = predict(url, appcode, img_base64data, configure)
    if stat != 200:
        print('Http status code: ', stat)
        print('Error msg in header: ',
              header['x-ca-error-message'] if 'x-ca-error-message' in header else '')
        print('Error msg in body: ', content)
        exit()
    result_str = content

    # print(result_str.decode(ENCODING))
    result = json.loads(result_str)
    for j in result['ret']:
        # print(j)
        print(j['word'])


if __name__ == '__main__':
    demo()
