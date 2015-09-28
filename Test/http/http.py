from urllib.parse import urlencode
from httplib2 import Http
import pymysql

http = Http()
headers={'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

conn = pymysql.Connect(host='192.168.120.12',user='root',passwd='123456',db='monitor_server',charset='utf8')
cur = conn.cursor()
sql="select * from ProtocolMonitor where status=0"
print(sql)
cur.execute(sql)
cur.close()
conn.close() 
for row in cur:
    method = row[2]
    url = row[3]
    body = row[4]
    response = row[5]
    frequence = row[6]
    print(method)
    print(url)
    print(response)
    print(frequence)
    resp, content = http.request(url,method,urlencode(body), headers=headers)
    print(resp)
    print(content)
    