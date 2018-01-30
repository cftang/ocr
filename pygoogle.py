#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line example for Custom Search.

Command-line application that does a search.
"""

__author__ = 'jcgregorio@google.com (Joe Gregorio)'

import re
import time
import img_utils
import ocrspace
import config

from googleapiclient.discovery import build

def main():
    time1 = time.time()
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    service = build("customsearch", "v1",
                    developerKey="AIzaSyD1ofgdmWhjp7ySXFlH5WlbS6LoBDIyolk")
    #question, answers = problem_utils.get_result()

    #img_utils.get_ios_img();

    question, answers = ocrspace.ocr_space_file(filename=config.IMAGE_PAGE, language='chs')

    time2 = time.time()

    print(question)
    print(answers)

    #question = u'「举杯邀明月,对影成三人」出自哪首诗',
    #answers = [u'《月下独酌》',u'《静夜思》',u'《赠汪伦》']
    #answers = [u'貂蝉',u'赵飞燕',u'杨玉环']
    #answers = [u'范曾', u'王世襄', u'黄永玉']
    qa = str(question)

    for s in answers:
        qa+=' '+str(s)

    # 判断否定
    is_opposite = (str(question).find(u"不") != -1)
    # 验证否定是否合法
    if is_opposite:
        # 不字前后没有未闭合的双引号或者书名号
        if re.match(u'^[^"《]*?((("[^"]+")|(《[^》]+》))[^"《]*)*不([^"》]*(("[^"]+")|(《[^》]+》)))*[^"》]*$',
                    re.sub(u'“|”', u'"', question)) is None:
            is_opposite = False

    res = service.cse().list(
        #q='UFO',
        #q='以下哪一个不是哆啦A梦的道具 记忆面包  魔女飞行扫帚 任意门',
        q=qa,
        #q='相传我国古代能作“掌上舞”的人是 赵飞燕  貂蝉 杨玉环',
        #q=u'以下哪个人不是中国著名画家 范曾 王世襄 黄永玉',
        cx='003126706661852603622:bz-lufnkvri',
    ).execute()

    time3 = time.time()

    body=''
    for result in res['items']:
        s=result['snippet']
        #print(s)
        body += s
    #print('item no:' + str(len(res['items'])))

    counts = []
    for answer in answers:
        num = body.count(answer)
        counts.append(num)
        print (answer + " ---> " + str(num))
    time4 = time.time()
    print('Elapsed '+str(time4-time1))
    print('Elapsed '+str(time2-time1))
    print('Elapsed '+str(time3-time2))
    #print('Elapsed '+str(time4-time3))


if __name__ == '__main__':
    main()