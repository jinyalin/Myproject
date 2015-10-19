# coding=utf8
import paramiko,datetime,os,threading
import time
import logging
runing = True
def InfoLog(message):
    format='%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='/home/ywget1/sftp_info.log', level=logging.INFO , format=format)
    logging.info(message)
def ErrorLog(message):
    format='%(asctime)s - %(pathname)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s'
    logging.basicConfig(filename='/home/ywget1/sftp_error.log', level=logging.ERROR , format=format)
    logging.error(message)
class run_cmd(threading.Thread):
      def __init__(self,hostname=None,username=None,pkey_file=None,port=None,echo_cmd=None):
          threading.Thread.__init__(self)
          self.hostname=hostname
          self.username=username
          self.pkey_file=pkey_file
          self.port=int(port)
          self.echo_cmd=echo_cmd
          self.thread_stop=False
      def run(self):
          paramiko.util.log_to_file('paramiko.log')
          s = paramiko.SSHClient()
          s.load_system_host_keys()
          s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
          key = paramiko.RSAKey.from_private_key_file(self.pkey_file,'&U*I(O1208')
          s.connect(self.hostname,self.port,self.username,pkey=key,timeout=10)
          stdin,stdout,stderr = s.exec_command(self.echo_cmd)
          for result in stdout.readlines():
              print result
              InfoLog("IP: "+self.hostname+" "+result.strip())
          s.close()
      def stop(self):
           self.thread_stop=True
class get_file(threading.Thread):
    def __init__(self,hostname=None,username=None,pkey_file=None,port=None,local_dir=None,remote_dir=None):
        threading.Thread.__init__(self)
        self.hostname=hostname
        self.port=int(port)
        self.username=username
        self.pkey_file=pkey_file
        self.local_dir=local_dir
        self.remote_dir=remote_dir
        self.thread_stop=False
    def run(self):
        try:
            t=paramiko.Transport((self.hostname,self.port))
            key = paramiko.RSAKey.from_private_key_file(self.pkey_file,'&U*I(O1208')
            t.connect(username=self.username,pkey=key)
            sftp=paramiko.SFTPClient.from_transport(t)
            print '--------------开始下载(get)文件---------------- %s ' % time.strftime('%Y-%m-%d %H:%M:%S')
            files=sftp.listdir(self.remote_dir)
            local_dir_new=self.local_dir+"/"+self.hostname+"_"+time.strftime("%Y%m%d%H%M%S")
            os.mkdir(local_dir_new)
            for f in files:
                if not f.startswith('.'):
                        print "正在从服务器%s下载文件 %s 到本地  %s" % (self.hostname,f,os.path.join(local_dir_new,f))
                        sftp.get(os.path.join(self.remote_dir,f),os.path.join(local_dir_new,f))
                        sftp.remove(os.path.join(self.remote_dir,f))
            print '-------------下载文件完成--------------- %s ' % time.strftime('%Y-%m-%d %H:%M:%S')
            t.close()
        except Exception,e:
            print e
    def stop(self):
        self.thread_stop=True
class upload_file(threading.Thread):
    def __init__(self,hostname=None,username=None,pkey_file=None,port=None,local_dir=None,remote_dir=None):
        threading.Thread.__init__(self)
        self.hostname=hostname
        self.port=int(port)
        self.username=username
        self.pkey_file=pkey_file
        self.local_dir=local_dir
        self.remote_dir=remote_dir
        self.thread_stop=False
    def run(self):
        try:
            t=paramiko.Transport((self.hostname,self.port))
            key = paramiko.RSAKey.from_private_key_file(self.pkey_file,'&U*I(O1208')
            t.connect(username=self.username,pkey=key)
            sftp=paramiko.SFTPClient.from_transport(t)
            print '--------------开始上传（upload）文件---------------- %s ' % time.strftime('%Y-%m-%d %H:%M:%S')
            files=os.listdir(self.local_dir)
            remote_dir_new=self.remote_dir+"/"+self.hostname+"_"+time.strftime("%Y%m%d%H%M%S")
            sftp.mkdir(remote_dir_new)
            for f in files:
                if not f.startswith('.'):
                    print "正在从本地服务器上传文件 %s 到服务器%s,远程路径： %s" % (f,self.hostname,os.path.join(remote_dir_new,f))
                    sftp.put(os.path.join(self.local_dir,f),os.path.join(remote_dir_new,f))
            print '-------------上传文件完成--------------- %s ' % time.strftime('%Y-%m-%d %H:%M:%S')
            t.close()
        except Exception,e:
                        print e
    def stop(self):
        self.thread_stop=True

while runing:
    username='bjywb'
    pkey_file='/home/ywget1/.ssh/hskj_20130620_bjywb'
    ip_file = '/hskj/script/ip.txt'
    print ("|--------------------------------|")
    print ("|     1 执行linux命令(cmd)       |")
    print ("|     2 下载文件(get)            |")
    print ("|     3 上传文件(put)            |")
    print ("|--------------------------------|")
    ten = int(raw_input('请选择:'))
    if type(ten) is not int:
       break
    else:
         if ten == 1:
            while runing:
               print ("    |--------------------------------------|")
               print ("    |     1 全部自有网关(cmpp|sgip|smgp)   |")
               print ("    |     2 全部移动网关（cmpp）           |")
               print ("    |     3 全部联通网关（sgip）           |")
               print ("    |     4 全部电信网关（smgp）           |")
               print ("    |     5 自定义服务器标识               |")
               print ("    |     0 返回上一级                     |")
               print ("    |--------------------------------------|")
               cmd_number = int(raw_input('请选择:'))
               if cmd_number == 0:
                   break
               if cmd_number == 1:
                  echo_cmd=raw_input('请输入要执行的linux命令:\n')
                  f = file(ip_file)
                  for line in f.readlines():
                      f.close()
                      if ("cmpp_" in line) or ("sgip_" in line) or ("smgp_" in line):
                        if ("HA" not in line) and ("vpn" not in line) and ("bak" not in line):
                            f_line = line.strip().split()
                            num = f_line[0]
                            hostname = f_line[2]
                            port = f_line[5]
                            if len(line) == 0:break
                            cmd_thread=run_cmd(hostname,username,pkey_file,port,echo_cmd)
                            print hostname
                            cmd_thread.start()
                            cmd_thread.stop()
                            if (cmd_thread.isAlive()):
                                cmd_thread.join()
               if cmd_number == 2:
                  echo_cmd=raw_input('请输入要执行的linux命令:\n')
                  f = file(ip_file)
                  for line in f.readlines():
                      f.close()
                      if "cmpp_" in line:
                        if ("HA" not in line) and ("vpn" not in line) and ("bak" not in line):
                            f_line = line.strip().split()
                            num = f_line[0]
                            hostname = f_line[2]
                            port = f_line[5]
                            if len(line) == 0:break
                            cmd_thread=run_cmd(hostname,username,pkey_file,port,echo_cmd)
                            print hostname
                            cmd_thread.start()
                            cmd_thread.stop()
                            if (cmd_thread.isAlive()):
                                cmd_thread.join()
               if cmd_number == 3:
                  echo_cmd=raw_input('请输入要执行的linux命令:\n')
                  f = file(ip_file)
                  for line in f.readlines():
                      f.close()
                      if "sgip_" in line:
                        if ("HA" not in line) and ("vpn" not in line) and ("bak" not in line):
                            f_line = line.strip().split()
                            num = f_line[0]
                            hostname = f_line[2]
                            port = f_line[5]
                            if len(line) == 0:break
                            cmd_thread=run_cmd(hostname,username,pkey_file,port,echo_cmd)
                            print hostname
                            cmd_thread.start()
                            cmd_thread.stop()
                            if (cmd_thread.isAlive()):
                                cmd_thread.join()
               if cmd_number == 4:
                  echo_cmd=raw_input('请输入要执行的linux命令:\n')
                  f = file(ip_file)
                  for line in f.readlines():
                      f.close()
                      if "smgp_" in line:
                        if ("HA" not in line) and ("vpn" not in line) and ("bak" not in line):
                            f_line = line.strip().split()
                            num = f_line[0]
                            hostname = f_line[2]
                            port = f_line[5]
                            if len(line) == 0:break
                            cmd_thread=run_cmd(hostname,username,pkey_file,port,echo_cmd)
                            print hostname
                            cmd_thread.start()
                            cmd_thread.stop()
                            if (cmd_thread.isAlive()):
                                cmd_thread.join()
               if cmd_number == 5:
                  server_id=raw_input('请输入服务器标识,多个之间用空格隔开,如：cmpp_220 smgp_60:\n')
                  echo_cmd=raw_input('请输入要执行的linux命令:\n')
                  server_list=server_id.split(' ')
                  f = file(ip_file)
                  for line in f.readlines():
                      f.close()
                      if '------' in line:continue
                      if line.count('\n')==len(line):continue
                      f_line = line.strip().split()
                      num = f_line[0]
                      hostname = f_line[2]
                      port = f_line[5]
                      if num in server_list:
                          cmd_thread=run_cmd(hostname,username,pkey_file,port,echo_cmd)
                          print hostname
                          cmd_thread.start()
                          cmd_thread.stop()
                          if (cmd_thread.isAlive()):
                                  cmd_thread.join()
                      if len(line) == 0:break
               else:
                    break
         if ten == 2:
            while runing:
                print ("    |---------------------------|")
                print ("    |     1 自定义服务器标识    |")
                print ("    |     0 返回上一级          |")
                print ("    |---------------------------|")
                cmd_number = int(raw_input('请选择:'))
                if cmd_number == 0:
                    break
                if cmd_number == 1:
                    server_id=raw_input('自定义服务器标识,多个之间用空格隔开:如：cmpp_220 smgp_60\n')
                    local_dir = "/home/ywget1/getdate"
                    remote_dir = "/hskj/tmp/bjywb/getdate"
                    server_list=server_id.split(' ')
                    f = file(ip_file)
                    for line in f.readlines():
                            f.close()
                            if '------' in line:continue
                            if line.count('\n')==len(line):continue
                            f_line = line.strip().split()
                            num = f_line[0]
                            hostname = f_line[2]
                            port = f_line[5]
                            if num in server_list:
                                    get_thread=get_file(hostname,username,pkey_file,port,local_dir,remote_dir)
                                    print hostname
                                    get_thread.start()
                                    get_thread.stop()
                                    if (get_thread.isAlive()):
                                            get_thread.join()
                            if len(line) == 0:break
                else:
                    break
         if ten == 3:
             while runing:
                 local_dir = "/home/ywget1/upload"
                 remote_dir = "/tmp"
                 print ("    |---------------------------------------|")
                 print ("    |    1 全部自有网关(cmpp|sgip|smgp)     |")
                 print ("    |    2 全部移动网关（cmpp）             |")
                 print ("    |    3 全部联通网关（sgip）             |")
                 print ("    |    4 全部电信网关（smgp）             |")                      
                 print ("    |    5 自定义服务器标识                 |")
                 print ("    |    0 返回上一级                       |")
                 print ("    |---------------------------------------|")
                 cmd_number = int(raw_input('请选择:'))
                 if cmd_number == 0:
                     break
                 if cmd_number == 5:
                     server_id=raw_input('自定义服务器标识,多个之间用空格隔开:如：cmpp_220 smgp_60\n')
                     server_list=server_id.split(' ')
                     f = file(ip_file)
                     for line in f.readlines():
                         f.close()
                         if '------' in line:continue
                         if line.count('\n')==len(line):continue
                         f_line = line.strip().split()
                         num = f_line[0]
                         hostname = f_line[2]
                         port = f_line[5]
                         if num in server_list:
                             upload_thread=upload_file(hostname,username,pkey_file,port,local_dir,remote_dir)
                             print hostname
                             upload_thread.start()
                             upload_thread.stop()
                             if (upload_thread.isAlive()):
                                 upload_thread.join()
                         if len(line) == 0:break
                     for up_file in os.listdir(local_dir):
                         os.remove(os.path.join(local_dir,up_file))
                 if cmd_number == 1:
                     f = file(ip_file)
                     for line in f.readlines():
                         f.close()
                         if ("cmpp_" in line) or ("sgip_" in line) or ("smgp_" in line):
                             if ("HA" not in line) and ("vpn" not in line) and ("bak" not in line):
                                 f_line = line.strip().split()
                                 num = f_line[0]
                                 hostname = f_line[2]
                                 port = f_line[5]
                                 if len(line) == 0:break
                                 upload_thread=upload_file(hostname,username,pkey_file,port,local_dir,remote_dir)
                                 print hostname
                                 upload_thread.start()
                                 upload_thread.stop()
                                 if (upload_thread.isAlive()):
                                     upload_thread.join()
                     for up_file in os.listdir(local_dir):
                         os.remove(os.path.join(local_dir,up_file))
                 if cmd_number == 2:
                     f = file(ip_file)
                     for line in f.readlines():
                         f.close()
                         if "cmpp_" in line:
                             if ("HA" not in line) and ("vpn" not in line) and ("bak" not in line):
                                 f_line = line.strip().split()
                                 num = f_line[0]
                                 hostname = f_line[2]
                                 port = f_line[5]
                                 if len(line) == 0:break
                                 upload_thread=upload_file(hostname,username,pkey_file,port,local_dir,remote_dir)
                                 print hostname
                                 upload_thread.start()
                                 upload_thread.stop()
                                 if (upload_thread.isAlive()):
                                     upload_thread.join()
                     for up_file in os.listdir(local_dir):
                         os.remove(os.path.join(local_dir,up_file))
                 if cmd_number == 3:
                     f = file(ip_file)
                     for line in f.readlines():
                         f.close()
                         if "sgip_" in line:
                             if ("HA" not in line) and ("vpn" not in line) and ("bak" not in line):
                                 f_line = line.strip().split()
                                 num = f_line[0]
                                 hostname = f_line[2]
                                 port = f_line[5]
                                 if len(line) == 0:break
                                 upload_thread=upload_file(hostname,username,pkey_file,port,local_dir,remote_dir)
                                 print hostname
                                 upload_thread.start()
                                 upload_thread.stop()
                                 if (upload_thread.isAlive()):
                                     upload_thread.join()
                     for up_file in os.listdir(local_dir):
                         os.remove(os.path.join(local_dir,up_file))
                 if cmd_number == 4:
                     f = file(ip_file)
                     for line in f.readlines():
                         f.close()
                         if "smgp_" in line:
                             if ("HA" not in line) and ("vpn" not in line) and ("bak" not in line):
                                 f_line = line.strip().split()
                                 num = f_line[0]
                                 hostname = f_line[2]
                                 port = f_line[5]
                                 if len(line) == 0:break
                                 upload_thread=upload_file(hostname,username,pkey_file,port,local_dir,remote_dir)
                                 print hostname
                                 upload_thread.start()
                                 upload_thread.stop()
                                 if (upload_thread.isAlive()):
                                     upload_thread.join()
                     for up_file in os.listdir(local_dir):
                         os.remove(os.path.join(local_dir,up_file))
                 else:
                     break
                    