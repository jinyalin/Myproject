'''
Created on 2014-4-2

@author: 1207263

'''

from urllib.parse import urlencode
from httplib2 import Http


http = Http()

url = "http://192.168.5.87:8080/post_report.do?"

body = {"corp_id": "6dcv002","user_id": "6dcv002","corp_pwd": "123456"} 

headers={'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

resp, content = http.request(url,"POST",urlencode(body), headers=headers)

print (content)
