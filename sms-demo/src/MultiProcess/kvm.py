import os,sys
ip_file = 'ip1.txt'
ip_dic = {}
num = 0
f = file(ip_file)
excution_list = []
for line in f.readlines():
    f_line = line.strip().split()
    num = line[0]
    host = line[1]
    port = line[2]
    if len(line) == 0:break
    ip_dic[num] = line
for k,v in ip_dic.items():
    print "%s. %s" %(k,v),
option = input("Please choose one server to connect:")
if option in ip_dic.keys():
    print ip_dic[option]
    cmd = 'ssh -i /home/yunwei/.ssh/hskj_20130606_bjxtb bjxtb@%s -p %s'  %(host,port)
    os.system(cmd)
        
