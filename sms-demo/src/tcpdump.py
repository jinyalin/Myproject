#!/usr/bin/python
#coding=UTF-8
import os,sys
import pexpect
reload(sys)
sys.setdefaultencoding('utf8')

if __name__=="__main__":
    while True:
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
        try:
            option = raw_input("请选择:\n")
            if option in ip_dic.keys():
                FILENAME = raw_input("请输入数据包文件名：\n")
                DUMP = ''
                while True:
                    DUMP = raw_input("请输入抓包命令，不写-w：\n")
                    if DUMP[0:7] != 'tcpdump':
                        print "您输入的不是抓包命令！"
                        continue
                    else:
                        break
                EMAIL = raw_input("请输入要接收的邮箱地址：\n")
                print ip_dic[option]
                ssh = pexpect.spawn(ip_dic[option])
                ssh.expect("key")
                ssh.sendline("&U*I(O1208")
                ssh.expect("$")
                cmd = "cd /hskj/tmp/bjywb/getdate &&"+ DUMP+" -w "+FILENAME+" && tar -Pzcvf "+ FILENAME+".tar.gz "+FILENAME+"  && /usr/local/bin/sendEmail -f nagios@baiwutong.com -t "+EMAIL+"  -s mail.baiwutong.com -u \"数据包\" -m \"附件为您抓取的数据包，请查收~\"  -a "+FILENAME+".tar.gz  -xu nagios@baiwutong.com  -xp hskj707   && rm -rf /hskj/tmp/bjywb/getdate/"+FILENAME+" /hskj/tmp/bjywb/getdate/"+FILENAME+".tar.gz  && echo "+name+"--`date '+%Y-%m-%d %H:%M:%S'`--Email  is  OK. | tee -a /hskj/tmp/bjywb/tcpdump.log"
                ssh.sendline(cmd)
                ssh.interact()
            else:
                print "您输入的服务器标识不存在！"
        except (Exception,SyntaxError,KeyboardInterrupt):
            print "您输入的内容存在问题，请重新输入!"