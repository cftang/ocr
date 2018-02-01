#!/usr/bin/python
# -*- coding: utf-8 -*-

import img_utils
import json
import re
import config
import requests
import time

def get_by_scan():
	question = '';
	answer = [];
	#questionLastLine = 0
	#识别文字
	#words = img_utils.spot()['words_result'];
	words = img_utils.spot()
	#isQuestion = True
	#问题
	'''
	if len(words) == 4:
	    question = words[0]['words'];
	elif len(words) >= 5:
	    question = words[0]['words'] + words[1]['words'];
	    flag = 2;
	question = question.replace("?","")
	'''
	questionLastLine=len(words)
	for i in range(0, len(words)):
		word = words[i]['words']
		if '/' in word:
			questionLastLine = i
			break

	#选项
	for i in range(0,questionLastLine):
		if i < questionLastLine-3:
			question +=words[i]['words']
		else:
			answer.append(words[i]['words'])
			#print u"选项" + str(i - questionLastLine) + u" : " +answer[i - questionLastLine-1]

	question = question.replace("?","")

	# python regex
	# http://blog.csdn.net/u014015972/article/details/51682536

	regex = u"^\d{0,2}\.?(.*)"

	person = re.findall(regex, question)
	question = person[0]

	result = []
	result.append(question)
	result.append(answer)
	return result

def get_chongding_by_api():
	#api_url = 'http://localhost/test.php'
	api_url = 'http://htpmsg.jiecaojingxuan.com/msg/current'
	req = requests.get(url=api_url)
	while(json.loads(req.text)['msg']  != u"成功"):
		time.sleep(0.5)
		req = requests.get(url=api_url)
	event = json.loads(req.text)['data']['event']
	question = event['desc'];
	answerStr = event['options']
	answerStr = answerStr.replace("\\\"","");
	answerStr = answerStr.replace("[","");
	answerStr = answerStr.replace("]","");
	answer = answerStr.split(",");

	result = []
	result.append(question)
	result.append(answer)
	return result

def get_result():
	if config.GET_TYPE == config.TYPE_NET_CHONGDING:
		return get_chongding_by_api()
	else:
		return get_by_scan()
