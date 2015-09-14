import webbrowser as web
import urllib2
import re
try:
    while 1:
        s = raw_input('please input your ip address :')
        if s == "" or s == 'exit':
            break
        else:
            url =  "http://www.ip138.com/ips138.asp?ip=%s&action=2" % s
            u = urllib2.urlopen(url)
            content = u.read().decode('gbk').encode('utf-8')
            ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', content)
            print "\n******from ip138 database******"
            print "ip address:",ip[0]
            result = re.findall(r'(<li>.*?</li>)',content.encode('UTF-8'))
            for i in result:
                print i[4:-5]
            print "*"*45
            print "\n"


except:
    print "not data fing"