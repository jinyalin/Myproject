from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views
import time
import os,sys
import paramiko
import threading

class worker(threading.Thread):
    def __init__(self,server=None,username=None,port=None,command=None,pkey_file=None,table_list=None):
        threading.Thread.__init__(self)
        self.server=server
        self.username=username
        self.port=port
        self.command=command
        self.pkey_file=pkey_file
        self.table_list=table_list
        print("11111111111111111111111111111111111")
        print(self.server)
        print(self.username)
        print (self.command)
        self.thread_stop=False
    def run(self):
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        key = paramiko.RSAKey.from_private_key_file(self.pkey_file)
        s.connect(self.server,self.port,self.username,pkey=key,timeout=10)
        stdin,stdout,stderr = s.exec_command(self.command)
        for result in stdout.readlines():
            self.table_list.append({'server':self.server,'content':result})
        s.close()
    def stop(self):
        self.thread_stop=True

                
def CommandQuery(req):
    if req.method == 'POST':
        type = req.REQUEST.get('type','cmpp')
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        print("开始时间："+str(NowTime))
        command = req.REQUEST.get('command','0')
        print("---command=-------"+command+"----------")
        username = 'bjxtb'
        pkey_file='/home/bjxtb/.ssh/id_rsa'
        conn,cur=ShareMethod.views.connDB_ssh()
        sql = "select server_ip,port from kvm_server_info where is_yw_ip = 1 and server_id like '%"+type+"%'"
        #sql = "select server_ip,port from kvm_server_info where is_yw_ip = 1 and (server_id like '%cmpp%')"
        print (sql)
        ShareMethod.views.exeQuery(cur,sql)
        ShareMethod.views.connClose(conn,cur)
        table_list = []
        for row in cur:
            server = row[0]
            port = row[1]
            print("jajajajajajajajaj")
            s = paramiko.SSHClient()
            s.load_system_host_keys()
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
            key = paramiko.RSAKey.from_private_key_file(pkey_file)
            s.connect(server,port,username,pkey=key,timeout=10)
            stdin,stdout,stderr = s.exec_command(command)
            for result in stdout.readlines():
                table_list.append({'server':server,'content':result})
#             cmd_thread=worker(server,username,port,command,pkey_file,table_list)
#             cmd_thread.setDaemon(True)
#             cmd_thread.start()
#         cmd_thread.join()
#         table_list = cmd_thread.table_list
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        print("结束时间："+str(NowTime))
        return render_to_response("CmdResult.html",locals())
    else:
        return render_to_response("CmdResult.html",locals())
        
        