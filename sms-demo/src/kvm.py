#!/usr/bin/python
#coding=UTF-8
import os,sys
import pexpect
reload(sys)
sys.setdefaultencoding('utf8')

if __name__=="__main__":
    lname = os.popen("id -un")
    name = lname.read().strip()
    dir = "/home/"+name
    user = "bjywb"
    ip_file = '/hskj/ip.txt'
    ip_dic = {}
    num = 0
    f = file(ip_file)
    excution_list = []
    for line in f.readlines():
        print line,
        if '------' in line:continue
        if line.count('\n')==len(line):continue
        f_line = line.strip().split()
        num = f_line[0]
        host = f_line[2]
        port = f_line[5]
        if len(line) == 0:break
        ip_dic[num] = 'ssh -o ServerAliveInterval=60 -i '+dir+'/.ssh/hskj_20130606_'+user+' '+user+'@%s -p %s'  %(host,port)
    option = raw_input("请选择:\n")
    if option in ip_dic.keys():
        print ip_dic[option]
        ssh = pexpect.spawn(ip_dic[option])
        ssh.expect("key")
        ssh.sendline("&U*I(O1208")
        ssh.expect("$")
        ssh.sendline("echo name "+name)
        ssh.interact()
    else:
        print "您输入的服务器标识不存在！"