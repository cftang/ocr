import requests
import json
import re

def ocr_space_file(filename, overlay=False, api_key='8df178c63588957', language='chs'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    #return r.content.decode()

    question = '';
    answer = [];
    questionLastLine = 0

    json1 = json.loads(r.content.decode())
    answerStr = json1['ParsedResults'][0]['ParsedText']
    #answerStr = answerStr.replace("\\\"","");
    words = answerStr.split("\r\n");

    for i in range(0, len(words)):
        word = words[i]
        if u'？' in word:
            questionLastLine = i
            break

    # 选项
    for i in range(0, len(words)):
        word = words[i]
        if i <= questionLastLine:
            question += word
        elif  '／' in word or len(word)==0:
            break
        else:
            answer.append(word)
        # print u"选项" + str(i - questionLastLine) + u" : " +answer[i - questionLastLine-1]

    question = question.replace("？", "")

    # python regex
    # http://blog.csdn.net/u014015972/article/details/51682536

    regex = u"^\d{0,2}\.?(.*)"

    person = re.findall(regex, question)
    question = person[0]

    result = []
    result.append(question)
    result.append(answer)
    return result


def ocr_space_url(url, overlay=False, api_key='helloworld', language='eng'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()


# Use examples:
#question,answer = ocr_space_file(filename='img.jpg', language='chs')
#test_url = ocr_space_url(url='http://i.imgur.com/31d5L5y.jpg')
#print (question)
#print (answer)
