# -*- coding: utf-8 -*-
from django.template.loader import get_template
from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
import ShareMethod.views

def select(req):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search','0')
    value=req.REQUEST.get('value','0')
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')
    
    sql= "select * from notice_info where 1 =1 "
    sql2 = "select count(*) as count from notice_info where 1=1 "
    
    if(search=='comment'):
        sql += " and comment like '%" + value + "%'"
        sql2 += " and comment like '%" + value + "%'"
    if(search=='content'):
        sql += " and content like '%" + value + "%'"
        sql2 += " and content like '%" + value + "%'"
    if(search=='alarm_value'):
        conn4,cur4=ShareMethod.views.connDB()
        sql4="select user_id,mobile,email from user_info where user_name like '%"+value+"%'"
        ShareMethod.views.exeQuery(cur4,sql4)
        for row4 in cur4:
            sql += " and (alarm_value like '%"+row4[0]+"%' or alarm_value like '%"+row4[1]+"%' or alarm_value like '%"+row4[2]+"%') "
            sql2 += " and (alarm_value like '%"+row4[0]+"%' or alarm_value like '%"+row4[1]+"%' or alarm_value like '%"+row4[2]+"%') "
        ShareMethod.views.connClose(conn4,cur4)
    if(search=='alarm_type'):
        if value=='邮件':
            sql += " and alarm_type like '%email%' "
            sql2 += " and alarm_type like '%email%' "
        if value=='电话':
            sql += " and alarm_type like '%phone%' "
            sql2 += " and alarm_type like '%phone%' "
        if value=='短信':
            sql += " and alarm_type like '%sms%' "
            sql2 += " and alarm_type like '%sms%' "
        if value=='弹屏':
            sql += " and alarm_type like '%screen%' "
            sql2 += " and alarm_type like '%screen%' "
        if value=='APP' or value=='app':
            sql += " and alarm_type like '%APP%' "
            sql2 += " and alarm_type like '%APP%' "
            
    if startTime!=endTime:
        if startTime!='':
            sql +=" and insert_time >='"+startTime+"'"
            sql2 +=" and insert_time >='"+startTime+"'"
        if endTime!='':
            sql +=" and insert_time <='"+endTime+"'"
            sql2 +=" and insert_time <='"+endTime+"'"
    else:
        if startTime!='':
            sql +=" and insert_time like '%"+startTime+"%'"
            sql2 +=" and insert_time like '%"+startTime+"%'"
    sql += " order by insert_time desc "
    
    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
            print(sql2)
            ShareMethod.views.connClose(conn2,cur2)
        
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)

    print(curPage)
    print(allPage)
    conn,cur=ShareMethod.views.connDB()
    conn3,cur3=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,sql) 
    for row in cur:
        alarmValueList = []
        if row[2]=='sms' or row[2]=='phone':
            alarmList=row[3].split(",")
            for alarm in alarmList:
                sql3="select user_name from user_info where mobile='"+alarm+"'"
                ShareMethod.views.exeQuery(cur3,sql3)
                for name in cur3:
                    alarmValueList.append(name[0])
            delimiter = ','
            alarm_value = delimiter.join(alarmValueList)
        if row[2]=='screen' or row[2]=='app':
            alarmList=row[3].split(",")
            for alarm in alarmList:
                sql3="select user_name from user_info where user_id='"+alarm+"'"
                ShareMethod.views.exeQuery(cur3,sql3)
                for name in cur3:
                    alarmValueList.append(name[0])
            delimiter = ','
            alarm_value = delimiter.join(alarmValueList) 
        if row[2]=='email':
            alarmList=row[3].split(",")
            for alarm in alarmList:
                sql3="select user_name from user_info where email='"+alarm+"'"
                ShareMethod.views.exeQuery(cur3,sql3)
                for name in cur3:
                    alarmValueList.append(name[0])
            delimiter = ','
            alarm_value = delimiter.join(alarmValueList) 
        table_list.append({'id':row[0],'content':row[1],'alarm_type':row[2],'alarm_value':alarm_value,'comment':row[4],'status':row[5],'insert_time':row[7]})
    ShareMethod.views.connClose(conn,cur)
    ShareMethod.views.connClose(conn3,cur3)
    return render_to_response('NIselect.html',locals())