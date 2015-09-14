'''
Created on 2014-4-2

@author: 1207263
'''




from urllib.parse import urlencode
from httplib2 import Http

http = Http()

url = "http://192.168.5.87:8080/sms_count2.do?"

body = {"corp_id": "6dcv002",
        "corp_pwd": "123456"} 

headers={'Content-Type': 'application/x-www-form-urlencoded;charset=gbk'}

resp, content = http.request(url,"POST",urlencode(body), headers=headers)

'''print (resp)'''

print (content)