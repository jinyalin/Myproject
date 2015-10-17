#!/usr/bin/python
# coding=UTF-8
import os,sys,time
import logging
#------变量部分------
#-----------start----------
#数据库名
DBname = 'cmpp_server'
#连接数据库的使用的账号和密码
mysqlConn="mysql -udba -psmshskj1207"
#测试用的联通手机号
un_mobile="15652087738"
#测试用的电信手机号
cm_mobile="15811491455"
#测试用的移动手机号
cdma_mobile="15321906869"
#弹屏通知用户工号,业务运维同事工号。
screenuser="1112196,1304333,1012079,1507502,1505480,1506493"
#-----------end-------------
def InfoLog(message):
    format='%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='log/info.log', level=logging.INFO , format=format)
    logging.info(message)
def ErrorLog(message):
    format='%(asctime)s - %(pathname)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s'
    logging.basicConfig(filename='log/error.log', level=logging.ERROR , format=format)
    logging.error(message)
num = 0
while True:
    tsn = os.popen(mysqlConn+" -e \"use "+DBname+";show table status like 'td_info';\"  | grep -v \"Name\" | awk '{print $11}'")
    Sn = tsn.read().strip()
    MaxSn = int(Sn)-1
    if MaxSn > num and num == 0:
        num = MaxSn
    else:
        if MaxSn > num:
            message = mysqlConn+" -e \"use "+DBname+";select td_code,td_name,ext from td_info where sn="+str(MaxSn)+";\" | grep -v \"td_code\""
            td_code_tmp = os.popen(message + "| awk  '{print $1}'")
            td_code = td_code_tmp.read().strip()
            td_name_tmp = os.popen(message + "| awk  '{print $2}'")
            td_name = td_name_tmp.read().strip()
            ext_tmp1 = os.popen(message + "| awk  '{print $3}'")
            ext_tmp2 = ext_tmp1.read().strip()
            ext = ext_tmp2.ljust(20,"4")
            if "发联通" in td_name:
                mobile = un_mobile
            if "发电信" in td_name:
                mobile = cdma_mobile
            if "发移动" in td_name:
                mobile = cm_mobile
            sql = "insert into submit_message_test(user_sn ,user_id ,sp_number ,mobile,msg_content,msg_id,yw_code ,status,response,insert_time,update_time,pknumber,pktotal ,sub_msg_id,charge_count ,msg_format,check_user,filter_flag,receive_time ,scan_time ,check_time,cache_sn,content ,md5_index ,fail_desc ,src_number,src_yw_code,ori_mobile) values (999999,'999999','"+ext+"','"+mobile+"','"+td_name+"---通道测试','0203121525_16361_39670',"+td_code+",1,0,now(),now(),0,0,0,1,8 ,'autotest' ,3,now(),now(),now(),0,'','','','"+ext+"',"+td_code+",'"+mobile+"')"
            cmd = mysqlConn+" -e \"use "+DBname+";"+sql+";\""
            try:
                os.system(cmd)
                num = MaxSn
                os.system("curl --data 'account=yunwei&passwd=123&screenwarning=1&screenuser="+screenuser+"&content=【新通道已完成单条测试】--> 通道名称:"+td_name+"，测试号码："+mobile+"，可到平台查看状态报告。'  http://yj.baiwutong.com:8180/PlateWarning")
                InfoLog("通道名称:"+td_name+"，测试号码："+mobile+"，已完成测试。")
            except Exception as e:
                ErrorLog(e) 
    time.sleep(10)