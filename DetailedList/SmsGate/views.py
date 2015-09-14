from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views
import time
import os

def select_gate(req,dbname,html,type,usertable):
    flag=req.REQUEST.get('flag','0')
    print("---flag=-------"+flag+"----------")
    if flag == '1':
        allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
        pageType = req.REQUEST.get('pageType','0')
        curPage = int(req.REQUEST.get('curPage','1'))
        allPage = int(req.REQUEST.get('allPage','1'))
        user_id=req.REQUEST.get('user_id','0')
        sp_number=req.REQUEST.get('sp_number','0')
        email=req.REQUEST.get('email','0')
        server = req.REQUEST.get('server','0')
        print("server:%s,user_id:%s"%(server,user_id))
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        startTime=req.REQUEST.get('startTime','0')
        endTime=req.REQUEST.get('endTime','0')
        user_sn = '0'
        conn3,cur3=ShareMethod.views.connDB_yw(server,dbname)
        sql3 = "select user_sn from "+usertable+" where user_id='"+user_id+"' limit 1"
        ShareMethod.views.exeQuery(cur3,sql3)
        for row3 in cur3:
            user_sn = row3[0]
        sql_1 = "select sp_number,mobile,msg_receiveTime,msg_reportTime,msg_id,response,1000,'未知',charge_count,replace(replace(replace(replace(msg_content,char(47),''),char(10),''),char(13),''),char(92),'') as msg_content  from submit_message_send_catch  where user_sn= "
        sql_2 = "select sp_number,mobile,msg_receiveTime,msg_reportTime,msg_id,response,err,fail_desc,charge_count,replace(replace(replace(replace(msg_content,char(47),''),char(10),''),char(13),''),char(92),'') as msg_content  from submit_message_send_history  where user_sn= "
        sql_3 = "select count(*) as count from submit_message_send_catch where user_sn= "
        sql_4 = "select count(*) as count from submit_message_send_history where user_sn= "
        sql_1 += str(user_sn)
        sql_2 += str(user_sn)
        sql_3 += str(user_sn)
        sql_4 += str(user_sn)
        
        if startTime!=endTime:
            if startTime!='':
                sql_1 +=" and msg_receiveTime >='"+startTime+"'"
                sql_2 +=" and msg_receiveTime >='"+startTime+"'"
                sql_3 +=" and msg_receiveTime >='"+startTime+"'"
                sql_4 +=" and msg_receiveTime >='"+startTime+"'"
            if endTime!='':
                sql_1 +=" and msg_receiveTime <='"+endTime+"'"
                sql_2 +=" and msg_receiveTime <='"+endTime+"'"
                sql_3 +=" and msg_receiveTime <='"+endTime+"'"
                sql_4 +=" and msg_receiveTime <='"+endTime+"'"
        else:
            if startTime!='':
                sql_1 +=" and msg_receiveTime like '"+startTime+"%'"
                sql_2 +=" and msg_receiveTime like '"+startTime+"%'"
                sql_3 +=" and msg_receiveTime like '"+startTime+"%'"
                sql_4 +=" and msg_receiveTime like '"+startTime+"%'"
                
        sql=sql_1+" union "+sql_2
        sql += " order by msg_receiveTime desc " 
        print(sql) 
        if allPostCounts == 0:
            conn1,cur1=ShareMethod.views.connDB_yw(server,dbname)
            conn2,cur2=ShareMethod.views.connDB_yw(server,dbname)
            ShareMethod.views.exeQuery(cur1,sql_3)
            ShareMethod.views.exeQuery(cur2,sql_4)
            for row1 in cur1:
                allPostCount1 = row1[0]
            for row2 in cur2:
                allPostCount2 = row2[0]

            allPostCounts=int(allPostCount1)+int(allPostCount2)
            
            ShareMethod.views.connClose(conn1,cur1)
            ShareMethod.views.connClose(conn2,cur2)
            
        table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    
        print(curPage)
        print(allPage)
        conn,cur=ShareMethod.views.connDB_yw(server,dbname)
        ShareMethod.views.exeQuery(cur,sql) 
        for row in cur:
            table_list.append({'sp_number':row[0],'mobile':row[1],'msg_receiveTime':row[2],'msg_reportTime':row[3],'msg_id':row[4],'response':row[5],'err':row[6],'fail_desc':row[7],'charge_count':row[8],'msg_content':row[9]})
        ShareMethod.views.connClose(conn,cur)
        server_list = select_server(req,type)
        return render_to_response(html,locals())
    else:
        server_list = select_server(req,type)
        print(server_list)
        return render_to_response(html,locals())

def select_cmpp(req):
    type = "cmpp"
    dbname = "cmpp_server"
    usertable = "cmpp_user"
    html = "SmsGate_cmpp.html"
    html = "SmsGate_cmpp.html"
    return select_gate(req,dbname,html,type,usertable)

def select_sgip(req):
    type = "sgip"
    dbname = "sgip_server"
    usertable = "sgip_user"
    html = "SmsGate_sgip.html"
    return select_gate(req,dbname,html,type,usertable)

def select_smgp(req):
    type = "smgp"
    dbname = "smgp_server_new"
    usertable = "smgp_user"
    html = "SmsGate_smgp.html"
    return select_gate(req,dbname,html,type,usertable)

def export_gate(req,dbname,direct,usertable):
    user = "bjxtb"
    path = "/tmp/"
    server = req.REQUEST.get('server','0')
    port = 22
    if server == '218.207.183.118':
        port = 10023
    if server == '61.147.118.16':
        port = 10002
    if server == '115.85.192.72':
        port = 10022
    
    print(server,dbname)
    operatorName=req.session.get('username')
    user_sn=req.REQUEST.get('user_sn','0')
    user_id=req.REQUEST.get('user_id','0')
    NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
    NowDate = time.strftime('%Y%m%d%H%M%S')
    startTime=req.REQUEST.get('startTime',NowTime)
    endTime=req.REQUEST.get('endTime',NowTime)
    email=req.REQUEST.get('email','0')
    if user_sn == '0' or user_sn == '':
        conn3,cur3=ShareMethod.views.connDB_yw(server,dbname)
        sql3 = "select user_sn from "+usertable+" where user_id='"+user_id+"' limit 1"
        print(sql3)
        ShareMethod.views.exeQuery(cur3,sql3)
        for row3 in cur3:
            user_sn = row3[0]
        print("user_sn="+user_sn)
        if user_sn == '0' or user_sn == '':
            return HttpResponseRedirect('../FailureMessage.do?message='+direct) 
    sql_1 = "select sp_number,mobile,msg_receiveTime,msg_reportTime,msg_id,response,1000,1000,charge_count,replace(replace(replace(replace(msg_content,char(47),''),char(10),''),char(13),''),char(92),'') as msg_content  from submit_message_send_catch  where user_sn= "
    sql_2 = "select sp_number,mobile,msg_receiveTime,msg_reportTime,msg_id,response,err,fail_desc,charge_count,replace(replace(replace(replace(msg_content,char(47),''),char(10),''),char(13),''),char(92),'') as msg_content  from submit_message_send_history  where user_sn= "
    sql_1 += str(user_sn)
    sql_2 += str(user_sn)
    
    if startTime!=endTime:
        if startTime!='':
            sql_1 +=" and msg_receiveTime >='"+startTime+"'"
            sql_2 +=" and msg_receiveTime >='"+startTime+"'"
        if endTime!='':
            sql_1 +=" and msg_receiveTime <='"+endTime+"'"
            sql_2 +=" and msg_receiveTime <='"+endTime+"'"
    else:
        if startTime!='':
            sql_1 +=" and msg_receiveTime like '"+startTime+"%'"
            sql_2 +=" and msg_receiveTime like '"+startTime+"%'"
            
    sql=sql_1+" union "+sql_2       
    
    FilePath1 = path+user_id+"_"+NowDate+".xls"
    TarPath = path+user_id+"_"+NowDate+".xls.tar.gz"
    
    sql += " into outfile '"+FilePath1+"'"
    print (sql)
    try:
        conn,cur=ShareMethod.views.connDB_yw(server,dbname)
        ShareMethod.views.exeQuery(cur,sql)
        ShareMethod.views.connClose(conn,cur)
        print("ssh "+user+"@"+server+" -p"+str(port)+" -o StrictHostKeyChecking=no tar -Pzcvf "+TarPath+" "+FilePath1)
        os.system("ssh "+user+"@"+server+" -p"+str(port)+" -o StrictHostKeyChecking=no tar -Pzcvf "+TarPath+" "+FilePath1)
        print("ssh "+user+"@"+server+" -p"+str(port)+" -o StrictHostKeyChecking=no /usr/local/bin/sendEmail -f nagios@baiwutong.com -t "+email+" -s mail.baiwutong.com -u '详单调取'   -a "+TarPath +" -xu nagios@baiwutong.com  -xp hskj707")
        os.system("ssh "+user+"@"+server+" -p"+str(port)+" -o StrictHostKeyChecking=no /usr/local/bin/sendEmail -f nagios@baiwutong.com -t "+email+" -s mail.baiwutong.com -u '详单调取'  -m '您好，附件为您提取的详单，请查阅~'  -a "+TarPath +" -xu nagios@baiwutong.com  -xp hskj707")
        
    except Exception as e:
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message='+direct)
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message='+direct)

def export_cmpp(req):
    dbname = "cmpp_server"
    direct = "SmsGate/select_cmpp.do"
    usertable = "cmpp_user"
    return export_gate(req,dbname,direct,usertable)

def export_sgip(req):
    dbname = "sgip_server"
    direct = "SmsGate/select_sgip.do"
    usertable = "sgip_user"
    return export_gate(req,dbname,direct,usertable)

def export_smgp(req):
    dbname = "smgp_server_new"
    direct = "SmsGate/select_smgp.do"
    usertable = "smgp_user"
    return export_gate(req,dbname,direct,usertable)


def select_server(req,type):   
    server_list = [] 
    conn,cur=ShareMethod.views.connDB_plate()
    sql = "select server_ip,server_id from server_info where status=0 and server_id like '%"+type+"%'"
    print(sql)
    ShareMethod.views.exeQuery(cur,sql)
    for row in cur:
        server_list.append({'ip':row[0],'server_name':row[1]})
    return server_list
        