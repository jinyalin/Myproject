# coding=utf8
import paramiko,datetime,os,threading
import logging
runing = True
def InfoLog(message):
    format='%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='log/info.log', level=logging.INFO , format=format)
    logging.info(message)    
def ErrorLog(message):
    format='%(asctime)s - %(pathname)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s'
    logging.basicConfig(filename='log/error.log', level=logging.ERROR , format=format)
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
              InfoLog(result)
          s.close()
      def stop(self):
           self.thread_stop=True
def main_cmd(line):
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
while runing:
    username='bjywb'
    pkey_file='/home/ywget1/.ssh/hskj_20130620_bjywb'
    ip_file = '/hskj/script/ip.txt'
    print ("1  执行cmd命令")
    print ("2 上传文件")
    print ("3 下载文件")
    ten = int(raw_input('请选择:'))
    if type(ten) is not int:
       break
    else:
         if ten == 1:
            while runing:
               print ("1 全部自有网关")
               print ("2 全部移动网关")
               print ("3 全部联通网关")
               print ("4 全部电信网关")
               print ("5 自定义IP")
               cmd_number = int(raw_input('请选择:'))
               if cmd_number == 1:
                  echo_cmd=raw_input('请输入要执行的linux命令:')
                  f = file(ip_file)
                  for line in f.readlines():
                      f.close()
                      if ("cmpp_" in line) or ("sgip_" in line) or ("smgp_" in line):
                          main_cmd(line)
               if cmd_number == 2:
                  echo_cmd=raw_input('请输入要执行的linux命令:')
                  f = file(ip_file)
                  for line in f.readlines():
                      f.close()
                      if "cmpp_" in line:
                          main_cmd(line)
               if cmd_number == 3:
                  echo_cmd=raw_input('请输入要执行的linux命令:')
                  f = file(ip_file)
                  for line in f.readlines():
                      f.close()
                      if "sgip_" in line:
                          main_cmd(line)
               if cmd_number == 4:
                  echo_cmd=raw_input('请输入要执行的linux命令:')
                  f = file(ip_file)
                  for line in f.readlines():
                      f.close()
                      if "smgp_" in line:
                          main_cmd(line)
               if cmd_number == 5:
                  ip=raw_input('请输入IP地址,多个IP用空格隔开:')
                  echo_cmd=raw_input('请输入要执行的linux命令:')
                  host=ip.split(' ')
                  f = file(ip_file)
                  for line in f.readlines():
                      f.close()
                      for hostname in host:
                          if hostname in line:
                              main_cmd(line)
               else:
                    break