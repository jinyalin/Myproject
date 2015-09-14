'''
Created on 2014-4-15

@author: 1207263


'''
# coding=UTF-8

from urllib.parse import urlencode
from httplib2 import Http

http = Http()

url = "http://192.168.5.87:8080/hSmsSend.do"

body = {"corp_id": "6dcv002",
        "corp_pwd": "123456",
        "corp_service": "23156384",
        "total_count": "2",
        "send_param": "13876682955&split&20110608122535&split&100&split&尊敬的会员张三您好，您的账户余额20元0&group&13876682955&split&20110608122535&split&100&split&尊敬的会员李四您好，您的账户余额2元",
        "ctrl_param": "1",} 

headers={'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}

resp, content = http.request(url,"POST",urlencode(body), headers=headers)

'''print (resp)'''

print (content)