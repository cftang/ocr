#!/usr/bin/python
# -*- coding: utf-8 -*-

from aip import AipOcr
from PIL import ImageGrab
import config
import json
from PIL import Image
import matplotlib.pyplot as plt
import datetime
client = AipOcr(config.APP_ID, config.API_KEY, config.SECRET_KEY)
import os

#通过adb获取android图像
def get_android_img():
    os.system('adb shell screencap -p /sdcard/screenshot.png')
    os.system('adb pull /sdcard/screenshot.png .')
    crop()

#获取ios图像
def get_ios_img():
    import shutil
    import os
    import time
    import wda
    from PIL import Image

    c = wda.Client('http://169.254.19.2:8100')  # DEVICE_URL
    #c = wda.Client('http://192.168.3.11:8100')  # DEVICE_URL

    c.screenshot('1.png')

    screenshot_backup_dir = 'screenshot_backups/'
    if not os.path.isdir(screenshot_backup_dir):
        os.mkdir(screenshot_backup_dir)

    img = Image.open('1.png')
    width, height = img.size
    # 冲顶大会
    newHeight = int(height * 0.65)

    # （left, upper, right, lower）

    box = (0, 200, width, newHeight)
    region = img.crop(box)
    region.save(config.IMAGE_PAGE)

    ts = int(time.time())
    shutil.copy(config.IMAGE_PAGE, '{}{}.png'.format(screenshot_backup_dir, ts))

def get_ios_img2():
    img = ImageGrab.grab()
    #TODO 截取区域可以调整
    box = (0, 300, 850, 1000)
    img = img.crop(box)
    img.save(config.IMAGE_PAGE_TEMP)

#裁剪图像
def crop():
    img = Image.open(config.IMAGE_PAGE)
    plt.figure("beauty")
    plt.subplot(1, 2, 1), plt.title('origin')
    plt.imshow(img), plt.axis('off')
    #TODO 截取区域可以调整
    box = (0, 300, 760, 900)
    roi = img.crop(box)
    roi.save(config.IMAGE_PAGE_TEMP);


#百度ocr获取图片位置
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

#识别文字
def spot():
    #get_ios_img();
    #crop();
    image = get_file_content(config.IMAGE_PAGE);
    result = client.basicGeneral(image);
    return result
