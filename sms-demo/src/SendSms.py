'''
Created on 2014-4-2

@author: 1207263
'''

# coding=UTF-8

from urllib.parse import urlencode
from httplib2 import Http

http = Http()

#url = "http://cloud.hongshutech.com:8080/sms_send2.do?"
#url = "http://cloud.baiwutong.com:8080/post_sms.do?"
#url = "http://service2.baiwutong.com:8080/sms_send2.do?"
#url = "http://flow.hbsmservice.com:8080/flow_interface/cClientFlowOrderInfo.do?"
url = "http://voicode.hongshutech.com:8888/VoiceClient/voiceCode.do?"
#msg_content = 'hehe'

# body = {"id": "jiankong",
#         "MD5_td_code": "jiankong",
#         #"corp_service": "td",
#         "mobile": "13261289750",
#         "msg_content": msg_content,
#         #"corp_msg_id": "",
#         "msg_id":"",
#         "ext": "",}
#NowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
# body = {"timeStamp":"20150627113805",
#         "userId":"jiankong",
#         "userPwd": "jiankong",
#         "mobile":"13261289750",
#         "orderMmount":"6",
#         "orderTime":"1",
#         "serviceCode":"td",
#         "msgId":"123456",
#         "extend":""
#         }

body = {"accountSid":"jiankong",
        "signature":"990824397ec95094748de167cea63daa",
        "operaType":"voiceCode",
        "serviceCode":"td",
        "callNumber":"4006081066",
        "voiceCode":"123456",
        "destNumber":"13261289750",
        "fetchDate":"20150903165826"
        }

headers={'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

resp, content = http.request(url,"POST",urlencode(body), headers=headers)
print(url,body)
print (resp,content)

print (content)