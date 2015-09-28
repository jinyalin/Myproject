from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
import ShareMethod.views
from test.test_typechecks import Integer

class MonitorInfo(forms.Form):
    monitor_sql = forms.CharField()
    warning_content = forms.CharField()
    comment = forms.CharField()
    expect_result = forms.CharField()
    type = forms.CharField()
    expect_result = forms.CharField()
    alarm_type = forms.CharField()

def insert(req):
    type=req.REQUEST.get('type',0)
    alarm_type=req.REQUEST.get('alarm_type','sms')
    if req.method == 'POST':
        form = MonitorInfo(req.POST)
        if form.is_valid():
            monitor_sql=form.cleaned_data['monitor_sql']
            warning_content=form.cleaned_data['warning_content']
            comment=form.cleaned_data['comment']
            expect_result=form.cleaned_data['expect_result']
            conn,cur=ShareMethod.views.connDB()
            sql="insert into monitor_info(monitor_sql,warning_content,comment,type,expect_result,alarm_type) values ("+monitor_sql+"," + warning_content +","+comment+","+type+","+expect_result+","+alarm_type+")"
            print(sql)
            ShareMethod.views.exeInsert(cur,sql)
            ShareMethod.views.connClose(conn,cur) 
            return render_to_response('MImessage.html',{'message':"添加成功"})
    else:
        form = MonitorInfo()
        return render_to_response('MIinsert.html')

def update(req):
    id=req.REQUEST.get('id',0)
    print(id)
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,"select * from monitor_info where sn="+id)
    MonitorInfo_list = []
    for row in cur:
        MonitorInfo_list.append({'id':row[0],'monitor_sql':row[1],'warning_content':row[2],'comment':row[3],'type':row[4],'expect_result':row[5],'alarm_type':row[6]})
    print(MonitorInfo_list)
    return render_to_response('MIedit.html',{'MonitorInfo_list':MonitorInfo_list})
    

def modify(req):
    id=req.REQUEST.get('id',0)
    monitor_sql=req.REQUEST.get('monitor_sql',0)
    warning_content=req.REQUEST.get('warning_content','0')
    comment=req.REQUEST.get('comment','0')
    type=req.REQUEST.get('type',0)
    expect_result=req.REQUEST.get('expect_result','0')
    alarm_type=req.REQUEST.get('alarm_type','0')
    #print(id)
    conn,cur=ShareMethod.views.connDB()
    sql="update monitor_info set monitor_sql='"+monitor_sql+"',warning_content='"+warning_content+"',comment='"+comment+"',type='"+type+"',expect_result='"+expect_result+"',alarm_type='"+alarm_type+"' where sn="+id
    print(sql)
    ShareMethod.views.exeUpdate(cur,sql)
    ShareMethod.views.connClose(conn,cur) 
    return render_to_response('MImessage.html',{'message':"修改成功"})
        
def delete(req): 
    id=req.REQUEST.get('id',0)
    print(type(id))
    print(id)
    conn,cur=ShareMethod.views.connDB()
    sql="delete from monitor_info where sn="+id
    print(sql)
    ShareMethod.views.exeDelete(cur,sql)
    ShareMethod.views.connClose(conn,cur)
    return render_to_response('MImessage.html',{'message':"删除成功"})

def select(req):
    search=req.REQUEST.get('search','0')
    value=req.REQUEST.get('value','0')
    type=req.REQUEST.get('type','0')
    print(search)
    print(value)
    conn,cur=ShareMethod.views.connDB()
    sql= "select * from monitor_info where 1 =1 and type='"+type+"'"
    if(search=='monitor_sql'):
        sql += " and monitor_sql like '%" + value + "%'"
    if(search=='warning_content'):
        sql += " and warning_content like '%" + value + "%'"
    if(search=='comment'):
        sql += " and comment like '%" + value + "%'"
    if(search=='alarm_type'):
        sql += " and alarm_type like '%" + value + "%'"
    ShareMethod.views.exeQuery(cur,sql) 
    ShareMethod.views.connClose(conn,cur) 
    contact_list = []
    for row in cur:
        contact_list.append({'id':row[0],'monitor_sql':row[1],'warning_content':row[2],'comment':row[3],'type':row[4],'expect_result':row[5],'alarm_type':row[6]})
    content_list,page_range = ShareMethod.views.pagination(req, contact_list)
    print(content_list)
    if(type=='0'):
        return render_to_response('MIselect_sql.html',{'MonitorInfo_list':content_list,'page_range':page_range})
    else:
        return render_to_response('MIselect_linux.html',{'MonitorInfo_list':content_list,'page_range':page_range})
     
