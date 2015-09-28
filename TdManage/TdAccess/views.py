# coding=UTF-8
from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views
import pymysql,xlrd
import time

def connDB(server_ip,port,dbname):
    conn=  pymysql.connect(host=server_ip,port=port,user='hs',passwd='V1ja89zab',db=dbname,charset='utf8')
    cur = conn.cursor()
    return (conn,cur)

def exeQuery(cur,sql):
    cur.execute(sql)
    return(cur)

def exeInsert(cur,sql):
    cur.execute(sql)
    return(cur)

def connClose(conn,cur):
    cur.close()
    conn.close()  
    
if __name__ == '__main__':
    data = xlrd.open_workbook('/tmp/cmpp-220.xls')
    table = data.sheet_by_name(u'Sheet1')
    nrows = table.nrows
    ncols = table.ncols
    for i in range(1,nrows):
        ext = table.cell(i,0).value
        td_name = table.cell(i,1).value
        server_ip = table.cell(i,2).value
        protocal = table.cell(i,3).value
        gate_ip = table.cell(i,4).value
        gate_port = table.cell(i,5).value
        gate_user = table.cell(i,6).value
        gate_pwd = table.cell(i,7).value
        gate_corp_code = table.cell(i,8).value
        gate_server_id = table.cell(i,9).value
        gate_max_connect = table.cell(i,10).value
        gate_max_speed = table.cell(i,11).value
        sgip_node_id = table.cell(i,12).value
        sgip_local_port = table.cell(i,13).value
        print(ext,td_name,server_ip,protocal,gate_ip,gate_port,gate_user,gate_pwd,gate_corp_code,gate_server_id,gate_max_connect,gate_max_speed,sgip_node_id,sgip_local_port)
        thread_param = "<param gate_ip='"+gate_ip+"' gate_port='"+gate_port+"' gate_user='"+gate_user+"' gate_pwd='"+gate_pwd+"' gate_corp_code='"+gate_corp_code+"' gate_server_id='"+gate_server_id+"' gate_max_connect='"+gate_max_connect+"' gate_max_speed='"+gate_max_speed+"' sgip_node_id='"+sgip_node_id+"' sgip_local_port='"+sgip_local_port+"' smgp_town_flow='0' smgp_country_flow='0' />"
        print(thread_param)
        submit_type = 1
        msg_count_all_en = 134
        msg_count_all_cn = 67
        dbname = ""
        if "SGIP" in protocal:
            thread_name = "com.hskj.sgip.api.SgipNioSendThread"
            submit_type = 3
            dbname = "sgip_server"
        if "SMGP" in protocal:
            thread_name = "com.hskj.smgp.api.Smgp30SendThread"
            dbname = "smgp_server_new"
        if "CMPP" in protocal:
            thread_name = "com.hskj.cmpp20.api.CmppSendThread"
            dbname = "cmpp_server"
        if "发联通" in td_name:
            td_type = '2'
            if "GS" in td_name:
                msg_count_all_cn = 66
                msg_count_all_en = 132
            if "FJ" in td_name:
                msg_count_all_cn = 65
                msg_count_all_en = 130
                
        if "发移动" in td_name:
            td_type = '1'
        if "发电信" in td_name:
            td_type = '3'
        t_sql = "select thread_id from thread_controller where sn = (select max(sn) from thread_controller)"
        print(t_sql)
        port = 3306
        conn1,cur1=connDB(server_ip,port,dbname)
        exeQuery(cur1,t_sql)
        thread_id1 = 0
        for row in cur1:
            thread_id1 = row[0]
        connClose(conn1,cur1)
        thread_id = int(thread_id1)+1
        thread_type = 1
        app_name = "Send"
        liveFlag = 0
        tstatus = 1
        status = 0
        filter_flag = 3
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        group_id = "2"
        td_code = group_id
        thread_sql = "insert into thread_controller (thread_name,thread_id,status,thread_param,thread_type,group_id,app_name,liveFlag) values ('"+thread_name+"',"+str(thread_id)+","+str(tstatus)+",\""+thread_param+"\","+str(thread_type)+","+str(group_id)+",'"+app_name+"',"+str(liveFlag)+")"
        print(thread_sql)
        conn2,cur2=connDB(server_ip,port,dbname)
        exeInsert(cur2,thread_sql)
        connClose(conn2,cur2)
        td_sql = "insert into td_info (td_name,td_type,td_code,status,ext,filter_flag,submit_type,msg_count_all_cn,msg_count_all_en) values('"+td_name+"','"+td_type+"','"+td_code+"',"+str(status)+",'"+ext+"',"+str(filter_flag)+","+str(submit_type)+","+str(msg_count_all_cn)+","+str(msg_count_all_en)+")"
        print(td_sql)
        conn3,cur3=connDB(server_ip,port,dbname)
        exeInsert(cur3,td_sql)
        connClose(conn3,cur3)
        remote_sn = "select sn from td_info where td_code='"+td_code+"'"
        print(remote_sn)
        conn4,cur4=connDB(server_ip,port,dbname)
        exeQuery(cur4,remote_sn)
        for row in cur4:
            remote_sn = row[0]
        connClose(conn4,cur4)
        server_id = "select server_id from server_info where server_ip ='"+server_ip+"'"
        conn5,cur5=connDB("210.14.134.77",13306,"super_plate")
        exeQuery(cur5,server_id)
        for row in cur5:
            remote_sn = row[0]
        connClose(conn5,cur5)
        local_td_sql = "insert into local_gate_td_info (td_name,td_type,td_code,status,ext,server_id,remote_sn,filter_flag,submit_type,insert_time,msg_count_all_cn,msg_count_all_en) values ('"+td_name+"',"+td_type+",'"+td_code+"',"+str(status)+",'"+ext+"','"+str(server_id)+"',"+str(remote_sn)+","+str(filter_flag)+","+str(submit_type)+",'"+NowTime+"',"+str(msg_count_all_cn)+","+str(msg_count_all_en)+")"
        print(local_td_sql)
        conn6,cur6=connDB("210.14.134.77",13306,"super_plate")
        exeInsert(cur6,local_td_sql)
        connClose(conn6,cur6)
        
        
        