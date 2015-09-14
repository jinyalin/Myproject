from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views
import time
import os

def select_SmsSp(req):
    flag=req.REQUEST.get('flag','0')
    print("---flag=-------"+flag+"----------")
    if flag == '1':
        allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
        pageType = req.REQUEST.get('pageType','0')
        curPage = int(req.REQUEST.get('curPage','1'))
        allPage = int(req.REQUEST.get('allPage','1'))
        dbname = 'sms_server'
        customer_id=req.REQUEST.get('customer_id','0')
        email=req.REQUEST.get('email','0')
        server = req.REQUEST.get('server','0')
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        startTime=req.REQUEST.get('startTime','0')
        endTime=req.REQUEST.get('endTime','0')
        print(server)
        sql = "select customer_id,code,dest_terminal_id,response_status,fail_describe,insert_time,update_time,msg_id,charge_count,msg_content from service_sms_info_catch where customer_id= "
        sql2 = "select count(*) as count from service_sms_info_catch where customer_id= "
        sql += "'"+customer_id+"' "
        sql2 += "'"+customer_id+"' "
        
        if startTime!=endTime:
            if startTime!='':
                sql +=" and insert_time >='"+startTime+"'"
                sql2 +=" and insert_time >='"+startTime+"'"
            if endTime!='':
                sql +=" and insert_time <='"+endTime+"'"
                sql2 +=" and insert_time <='"+endTime+"'"
        else:
            if startTime!='':
                sql +=" and insert_time like '"+startTime+"%'"
                sql2 +=" and insert_time like '"+startTime+"%'"
        sql += " order by insert_time desc "
        print(sql) 
        if allPostCounts == 0:
            conn2,cur2=ShareMethod.views.connDB_yw(server,'sms_server')
            ShareMethod.views.exeQuery(cur2,sql2)
            for row in cur2:
                allPostCounts = row[0]
                print(sql2)
            ShareMethod.views.connClose(conn2,cur2)
            
        table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    
        print(curPage)
        print(allPage)
        conn,cur=ShareMethod.views.connDB_yw(server,'sms_server')
        ShareMethod.views.exeQuery(cur,sql) 
        for row in cur:
            table_list.append({'customer_id':row[0],'code':row[1],'dest_terminal_id':row[2],'response_status':row[3],'fail_describe':row[4],'insert_time':row[5],'update_time':row[6],'msg_id':row[7],'charge_count':row[8],'msg_content':row[9]})
        ShareMethod.views.connClose(conn,cur)
        server_list = select_server(req,'sp')
        return render_to_response('SmsSp.html',locals())
    else:
        server_list = select_server(req,'sp')
        print (server_list)
        return render_to_response('SmsSp.html',locals())
    
def export(req,sql,dbname,direct):
    user = "bjxtb"
    path = "/tmp/"
    server = req.REQUEST.get('server','210.14.156.175')
    operatorName=req.session.get('username')
    customer_id=req.REQUEST.get('customer_id','0')
    NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
    NowDate = time.strftime('%Y%m%d%H%M%S')
    startTime=req.REQUEST.get('startTime',NowDate)
    endTime=req.REQUEST.get('endTime',NowDate)
    email=req.REQUEST.get('email','0')
    
    sql += "'"+customer_id+"' "
    
    if startTime!=endTime:
        if startTime!='':
            sql +=" and insert_time >='"+startTime+"'"
        if endTime!='':
            sql +=" and insert_time <='"+endTime+"'"
    else:
        if startTime!='':
            sql +=" and insert_time like '"+startTime+"%'"
            
    FilePath1 = path+customer_id+"_"+NowDate+".xls"
    TarPath = path+customer_id+"_"+NowDate+".xls.tar.gz"
    
    sql += " into outfile '"+FilePath1+"'"
    print (sql)
    try:
        conn,cur=ShareMethod.views.connDB_yw(server,dbname)
        ShareMethod.views.exeQuery(cur,sql)
        ShareMethod.views.connClose(conn,cur)
        print("ssh "+user+"@"+server+" tar -Pzcvf "+TarPath+" "+FilePath1)
        os.system("ssh "+user+"@"+server+" tar -Pzcvf "+TarPath+" "+FilePath1)
        print("ssh "+user+"@"+server+" /usr/local/bin/sendEmail -f nagios@baiwutong.com -t "+email+" -s mail.baiwutong.com -u '详单调取'   -a "+TarPath +" -xu nagios@baiwutong.com  -xp hskj707")
        os.system("ssh "+user+"@"+server+" /usr/local/bin/sendEmail -f nagios@baiwutong.com -t "+email+" -s mail.baiwutong.com -u '详单调取'  -m '您好，附件为您提取的详单，请查阅~'  -a "+TarPath +" -xu nagios@baiwutong.com  -xp hskj707")
        
    except Exception as e:
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message='+direct)
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message='+direct)


def export_SmsSp(req):
    dbname = 'sms_server'
    direct = "SmsSp/select_SmsSp.do"
    sql = "select customer_id,code,dest_terminal_id,response_status,fail_describe,insert_time,update_time,msg_id,charge_count,msg_content from service_sms_info_catch where customer_id= "
    return export(req,sql,dbname,direct)

def select_server(req,type):   
    server_list = [] 
    conn,cur=ShareMethod.views.connDB_plate()
    sql = "select server_ip,server_id from server_info where status=0 and server_id like '%"+type+"%' and server_id not like '%mms%'"
    print(sql)
    ShareMethod.views.exeQuery(cur,sql)
    for row in cur:
        server_list.append({'ip':row[0],'server_name':row[1]})
    return server_list