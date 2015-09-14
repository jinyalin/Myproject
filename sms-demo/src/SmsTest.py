#!/usr/bin/python
# coding=UTF-8
import os,sys,time
num = 0
DBname = 'cmpp_server'
while True:
    tsn = os.popen("mysql -udba -psmshskj1207 -e \"use cmpp_server;show table status like 'td_info';\"  | grep -v \"Name\" | awk '{print $11}'")
    Sn = tsn.read().strip()
    MaxSn = int(Sn)-1
    if MaxSn > num and num == 0:
        num = MaxSn
    else:
        if MaxSn > num:
            message = "mysql -udba -psmshskj1207 -e \"use "+DBname+";select td_code,td_name,ext from td_info where sn="+str(MaxSn)+";\" | grep -v \"td_code\""
            td_code1 = os.popen(message + "| awk  '{print $1}'")
            td_code = td_code1.read().strip()
            td_name1 = os.popen(message + "| awk  '{print $2}'")
            td_name = td_name1.read().strip()
            ext1 = os.popen(message + "| awk  '{print $3}'")
            ext = ext1.read().strip()
            if "发联通" in td_name:
                mobile = '13261289750'
            if "发电信" in td_name:
                mobile = '15321906869'
            if "发移动" in td_name:
                mobile = '15811491455'
            sql = "insert into submit_message_test(user_sn ,user_id ,sp_number ,mobile,msg_content,msg_id,yw_code ,status,response,insert_time,update_time,pknumber,pktotal ,sub_msg_id,charge_count ,msg_format,check_user,filter_flag,receive_time ,scan_time ,check_time,cache_sn,content ,md5_index ,fail_desc ,src_number,src_yw_code,ori_mobile) values (123,'','"+ext+"444','"+mobile+"','"+td_name+"---通道测试','0203121525_16361_39670',"+td_code+",1,0,now(),now(),0,0,0,1,8 ,'autotest' ,3,now(),now(),now(),0,'','','','"+ext+"444',"+td_code+",'"+mobile+"');"
            cmd = "mysql -udba -psmshskj1207 -e \"use "+DBname+";"+sql+";\""
            os.system(cmd)
            num = MaxSn
            os.system("/usr/local/bin/sendEmail -f nagios@baiwutong.com -t yunwei@baiwutong.com -s mail.baiwutong.com -u '通道自动化测试结果'  -m '"+td_name+"------测试完成~联通号码：15652087738，移动号码：15811491455，电信号码：15321906869 请到接入通道的服务器查看发送状态报告~'  -xu nagios@baiwutong.com  -xp hskj707")
    time.sleep(30)