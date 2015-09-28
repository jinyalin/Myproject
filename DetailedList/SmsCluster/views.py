from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views
import time
import os

def select_cluster(req):
    flag=req.REQUEST.get('flag','0')
    userid=req.session.get('userid')
    port=13306
    print("---flag=-------"+flag+"----------")
    if flag == '1':
        allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
        pageType = req.REQUEST.get('pageType','0')
        curPage = int(req.REQUEST.get('curPage','1'))
        allPage = int(req.REQUEST.get('allPage','1'))
        dbname = 'cluster_server'
        limit=req.REQUEST.get('limit','0')
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        NowDate = time.strftime('%Y-%m-%d')
        NowMonth = time.strftime('%Y%m')
        startTime=req.REQUEST.get('startTime','0')
        endTime=req.REQUEST.get('endTime','0')
        user_id=req.REQUEST.get('user_id','0')
        fail_desc=req.REQUEST.get('fail_desc','0')
        sql_select = "select user_id from all_user_info where server_id='cluster_64' and service_staff='"+userid+"'"
        print(sql_select)
        email=req.REQUEST.get('email','0')
        server = req.REQUEST.get('server','210.14.134.81')
        conn6,cur6=ShareMethod.views.connDB_plate()
        ShareMethod.views.exeQuery(cur6,sql_select)
        user_list = []
        for row6 in cur6:
            user_list.append(row6[0])
        print("user_id:"+user_id)
        print(user_list)
        if user_id in user_list:
            table_list=[]
            if startTime == NowDate:
                if limit == '20':
                    sql_1 = "select user_id,sp_number,msg_receive_time,msg_report_time,msg_id,mobile,response,fail_desc,charge_count,replace(replace(replace(replace(msg_content,char(47),''),char(10),''),char(13),''),char(92),'') as msg_content from submit_message_send_history  where user_id= "
                    sql_1 += "'"+user_id+"' "
                    if startTime!=endTime:
                        if startTime!='':
                            sql_1 +=" and insert_time >='"+startTime+"'"
                        if endTime!='':
                            sql_1 +=" and insert_time <='"+endTime+"'"
                    else:
                        if startTime!='':
                            sql_1 +=" and insert_time like '"+startTime+"%'"
                    if fail_desc !="" and fail_desc!='0':
                        sql_1 += " and fail_desc like '%"+fail_desc+"%' "
                    sql_1 += " limit 20 "
                    conn,cur=ShareMethod.views.connDB_yw(server,dbname,port)
                    ShareMethod.views.exeQuery(cur,sql_1) 
                    for row in cur:
                        table_list.append({'user_id':row[0],'sp_number':row[1],'msg_receive_time':row[2],'msg_report_time':row[3],'msg_id':row[4],'mobile':row[5],'response':row[6],'fail_desc':row[7],'charge_count':row[8],'msg_content':row[9]})
                    ShareMethod.views.connClose(conn,cur)
                    allPostCounts=20
                    return render_to_response('SmsCluster.html',locals())
                else:
                    sql_1 = "select user_id,sp_number,msg_receive_time,msg_report_time,msg_id,mobile,response,fail_desc,charge_count,replace(replace(replace(replace(msg_content,char(47),''),char(10),''),char(13),''),char(92),'') as msg_content from submit_message_send_catch  where user_id= "
                    sql_2 = "select user_id,sp_number,msg_receive_time,msg_report_time,msg_id,mobile,response,fail_desc,charge_count,replace(replace(replace(replace(msg_content,char(47),''),char(10),''),char(13),''),char(92),'') as msg_content from submit_message_send_history  where user_id= "
                    sql_3 = "select count(*) as count from submit_message_send_catch where user_id= "
                    sql_4 = "select count(*) as count from submit_message_send_history where user_id= "
                    
                    sql_1 += "'"+user_id+"' "
                    sql_2 += "'"+user_id+"' "
                    sql_3 += "'"+user_id+"' "
                    sql_4 += "'"+user_id+"' "
                    if startTime!=endTime:
                        if startTime!='':
                            sql_1 +=" and insert_time >='"+startTime+"'"
                            sql_2 +=" and insert_time >='"+startTime+"'"
                            sql_3 +=" and insert_time >='"+startTime+"'"
                            sql_4 +=" and insert_time >='"+startTime+"'"
                        if endTime!='':
                            sql_1 +=" and insert_time <='"+endTime+"'"
                            sql_2 +=" and insert_time <='"+endTime+"'"
                            sql_3 +=" and insert_time <='"+endTime+"'"
                            sql_4 +=" and insert_time <='"+endTime+"'"
                    else:
                        if startTime!='':
                            sql_1 +=" and insert_time like '"+startTime+"%'"
                            sql_2 +=" and insert_time like '"+startTime+"%'"
                            sql_3 +=" and insert_time like '"+startTime+"%'"
                            sql_4 +=" and insert_time like '"+startTime+"%'"
                            
                    sql=sql_1+" union "+sql_2
                    sql += " order by msg_receive_time desc " 
                    print (sql)
                    if allPostCounts == 0:
                        conn1,cur1=ShareMethod.views.connDB_yw(server,dbname,port)
                        conn2,cur2=ShareMethod.views.connDB_yw(server,dbname,port)
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
                    conn,cur=ShareMethod.views.connDB_yw(server,dbname,port)
                    ShareMethod.views.exeQuery(cur,sql) 
                    for row in cur:
                        table_list.append({'user_id':row[0],'sp_number':row[1],'msg_receive_time':row[2],'msg_report_time':row[3],'msg_id':row[4],'mobile':row[5],'response':row[6],'fail_desc':row[7],'charge_count':row[8],'msg_content':row[9]})
                    ShareMethod.views.connClose(conn,cur)
                    return render_to_response('SmsCluster.html',locals())
            else:
                if limit == '20':
                    sql_1 = "select user_id,sp_number,msg_receive_time,msg_report_time,msg_id,mobile,response,fail_desc,charge_count,replace(replace(replace(replace(msg_content,char(47),''),char(10),''),char(13),''),char(92),'') as msg_content from submit_message_send_history_"+NowMonth+"  where user_id= "
                    sql_1 += "'"+user_id+"' "
                    if startTime!=endTime:
                        if startTime!='':
                            sql_1 +=" and insert_time >='"+startTime+"'"
                        if endTime!='':
                            sql_1 +=" and insert_time <='"+endTime+"'"
                    else:
                        if startTime!='':
                            sql_1 +=" and insert_time like '"+startTime+"%'"
                    if fail_desc !="" and fail_desc!='0':
                        sql_1 += " and fail_desc like '%"+fail_desc+"%' "
                    sql_1 += " limit 20 "
                    conn,cur=ShareMethod.views.connDB_yw(server,dbname,port)
                    ShareMethod.views.exeQuery(cur,sql_1) 
                    for row in cur:
                        table_list.append({'user_id':row[0],'sp_number':row[1],'msg_receive_time':row[2],'msg_report_time':row[3],'msg_id':row[4],'mobile':row[5],'response':row[6],'fail_desc':row[7],'charge_count':row[8],'msg_content':row[9]})
                    ShareMethod.views.connClose(conn,cur)
                    allPostCounts=20
                    return render_to_response('SmsCluster.html',locals())
                else:
                    sql = "select user_id,sp_number,msg_receive_time,msg_report_time,msg_id,mobile,response,fail_desc,charge_count,replace(replace(replace(replace(msg_content,char(47),''),char(10),''),char(13),''),char(92),'') as msg_content from submit_message_send_history_"+NowMonth+"  where user_id= "
                    sql_1 = "select count(*) as count from submit_message_send_history_"+NowMonth+" where user_id= "
                    sql += "'"+user_id+"' "
                    sql_1 += "'"+user_id+"' "
                    if startTime!=endTime:
                        if startTime!='':
                            sql +=" and insert_time >='"+startTime+"'"
                            sql_1 +=" and insert_time >='"+startTime+"'"
                        if endTime!='':
                            sql +=" and insert_time <='"+endTime+"'"
                            sql_1 +=" and insert_time <='"+endTime+"'"
                    else:
                        if startTime!='':
                            sql +=" and insert_time like '"+startTime+"%'"
                            sql_1 +=" and insert_time like '"+startTime+"%'"
                            
                    sql += " order by msg_receive_time desc " 
                    print (sql)
                    print(sql_1)
                    if allPostCounts == 0:
                        conn1,cur1=ShareMethod.views.connDB_yw(server,dbname,port)
                        ShareMethod.views.exeQuery(cur1,sql_1)
                        for row1 in cur1:
                            allPostCount1 = row1[0]
            
                        allPostCounts=int(allPostCount1)
                        
                        ShareMethod.views.connClose(conn1,cur1)
                        
                    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
                
                    print(curPage)
                    print(allPage)
                    conn,cur=ShareMethod.views.connDB_yw(server,dbname,port)
                    ShareMethod.views.exeQuery(cur,sql) 
                    for row in cur:
                        table_list.append({'user_id':row[0],'sp_number':row[1],'msg_receive_time':row[2],'msg_report_time':row[3],'msg_id':row[4],'mobile':row[5],'response':row[6],'fail_desc':row[7],'charge_count':row[8],'msg_content':row[9]})
                    ShareMethod.views.connClose(conn,cur)
                    return render_to_response('SmsCluster.html',locals())
        else:
            return render_to_response('SmsCluster.html',locals())
    else:
        return render_to_response('SmsCluster.html',locals())


def export_cluster(req):
    port=13306
    dbname = 'cluster_server'
    direct = "SmsCluster/select_cluster.do"
    user = "bjxtb"
    path = "/tmp/"
    operatorName=req.session.get('username')
    userid=req.session.get('userid')
    user_id=req.REQUEST.get('user_id','0')
    NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
    NowDate = time.strftime('%Y%m%d%H%M%S')
    startTime=req.REQUEST.get('startTime',NowDate)
    endTime=req.REQUEST.get('endTime',NowDate)
    email=req.REQUEST.get('email','0')
    sql_select = "select user_id from all_user_info where server_id='cluster_64' and service_staff='"+userid+"'"
    print(sql_select)
    email=req.REQUEST.get('email','0')
    server = req.REQUEST.get('server','210.14.134.81')
    conn6,cur6=ShareMethod.views.connDB_plate()
    ShareMethod.views.exeQuery(cur6,sql_select)
    user_list = []
    for row6 in cur6:
        user_list.append(row6[0])
    print("user_id:"+user_id)
    print(user_list)
    if user_id in user_list:
        sql_1 = "select user_id,sp_number,msg_receive_time,msg_report_time,msg_id,mobile,response,fail_desc,charge_count,replace(replace(replace(replace(msg_content,char(47),''),char(10),''),char(13),''),char(92),'') as msg_content from submit_message_send_catch  where user_id= "
        sql_2 = "select user_id,sp_number,msg_receive_time,msg_report_time,msg_id,mobile,response,fail_desc,charge_count,replace(replace(replace(replace(msg_content,char(47),''),char(10),''),char(13),''),char(92),'') as msg_content from submit_message_send_history  where user_id= "
        sql_1 += "'"+user_id+"' "
        sql_2 += "'"+user_id+"' "
        
        if startTime!=endTime:
            if startTime!='':
                sql_1 +=" and insert_time >='"+startTime+"'"
                sql_2 +=" and insert_time >='"+startTime+"'"
            if endTime!='':
                sql_1 +=" and insert_time <='"+endTime+"'"
                sql_2 +=" and insert_time <='"+endTime+"'"
        else:
            if startTime!='':
                sql_1 +=" and insert_time like '"+startTime+"%'"
                sql_2 +=" and insert_time like '"+startTime+"%'"
                
        sql=sql_1+" union "+sql_2       
        
        FilePath1 = path+user_id+"_"+NowDate+".xls"
        TarPath = path+user_id+"_"+NowDate+".xls.tar.gz"
        
        sql += " into outfile '"+FilePath1+"'"
        print (sql)
        try:
            conn,cur=ShareMethod.views.connDB_yw('210.14.134.81',dbname,port)
            ShareMethod.views.exeQuery(cur,sql)
            ShareMethod.views.connClose(conn,cur)
            server = "210.14.134.81"
            print("ssh "+user+"@"+server+" -p10065 tar -Pzcvf "+TarPath+" "+FilePath1)
            os.system("ssh "+user+"@"+server+" -p10065 tar -Pzcvf "+TarPath+" "+FilePath1)
            print("ssh "+user+"@"+server+" -p10065 /usr/local/bin/sendEmail -f nagios@baiwutong.com -t "+email+" -s mail.baiwutong.com -u '详单调取'   -a "+TarPath +" -xu nagios@baiwutong.com  -xp hskj707")
            os.system("ssh "+user+"@"+server+" -p10065 /usr/local/bin/sendEmail -f nagios@baiwutong.com -t "+email+" -s mail.baiwutong.com -u '详单调取'  -m '您好，附件为您提取的详单，请查阅~'  -a "+TarPath +" -xu nagios@baiwutong.com  -xp hskj707")
            
        except Exception as e:
            ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
            return HttpResponseRedirect('../FailureMessage.do?message='+direct)
        ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
        return HttpResponseRedirect('../SuccessMessage.do?message='+direct)
    else:
        return HttpResponseRedirect('../FailureMessage.do?message='+direct)