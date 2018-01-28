#!/usr/bin/python
# -*- coding: utf-8 -*-

import solve_utils
import problem_utils
import config
import time
import re
from sys import stdout

time_start = time.time()

#question, answers = problem_utils.get_result()
question = u'以下哪个人不是中国著名画家'
answers = [u'范曾',u'王世襄',u'黄永玉']

#question = u'十年树木，百年树人是谁说的'
#answers = [u'管仲',u'齐桓公',u'鲍叔牙']

#question = u'可以跳"掌中舞"的美女是谁'
#answers = [u'貂蝉',u'赵飞燕',u'杨玉环']

print(u"问题 ：" + question)
if not answers:
    raise ValueError(u'未能识别出答案选项'.encode(stdout.encoding))

# 选项
for i in range(0, len(answers)):
    print(u"选项" + str(i + 1) + u" : " + answers[i])

if config.OPEN_BROWSER:
    solve_utils.open_webpage(question)

# 判断否定
is_opposite = (question.find(u"不") != -1)
# 验证否定是否合法
if is_opposite:
    # 不字前后没有未闭合的双引号或者书名号
    if re.match(u'^[^"《]*?((("[^"]+")|(《[^》]+》))[^"《]*)*不([^"》]*(("[^"]+")|(《[^》]+》)))*[^"》]*$',
                re.sub(u'“|”', u'"', question)) is None:
        is_opposite = False


#http://masnun.com/2016/03/29/python-a-quick-introduction-to-the-concurrent-futures-module.html
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
 
pool = ThreadPoolExecutor(3)
futures = []
futures.append(pool.submit(solve_utils.words_count,question, answers))
futures.append(pool.submit(solve_utils.search_count,question, answers))

# 两种方式进行判断
#words_count = solve_utils.words_count(question, answers)
#search_count = solve_utils.search_count(question, answers)
#print(u'%-15s' * 3 % (u'', u'词频', u'结果数'))
#for answer, word_count, search_num in zip(answers, words_count, search_count):
#    print(u'%-15s' * 3 % (answer, word_count, search_num))

minValue=9
maxValue=-9

choose=[0,0,0]
for x in as_completed(futures):
    if is_opposite:
        for i in range(3):
            print(x.result()[i])
        minValue=min(x.result())
        for i in range(3):
            if minValue == x.result()[i]:
                print('choose ----' + str(i+1))
                break    
    else:
        for i in range(3):
            print(x.result()[i])
        maxValue=max(x.result())
        for i in range(3):
            if maxValue == x.result()[i]:
                print('choose ----' + str(i+1))
                break    
print(u'耗时：%s s' % (time.time() - time_start))
