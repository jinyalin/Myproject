from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
import ShareMethod.views

class ServerMonitorInfo(forms.Form):
    server_sn = forms.IntegerField()
    monitor_sn = forms.IntegerField()
    value = forms.IntegerField()
    make = forms.CharField()
    frequency = forms.CharField()
    last_time = forms.CharField()
    status = forms.IntegerField()
    type = forms.IntegerField()
'''
def insert(req):
    if req.method == 'POST':
        form = ServerMonitorInfo(req.POST)
        if form.is_valid():
            monitor_sql=form.cleaned_data['monitor_sql']
            warning_content=form.cleaned_data['warning_content']
            comment=form.cleaned_data['comment']
            type=form.cleaned_data['type']
            conn,cur=ShareMethod.views.connDB()
            sql="insert into monitor_info(monitor_sql,warning_content,comment,type) values ("+monitor_sql+"," + warning_content +","+comment+","+type+")"
            print(sql)
            ShareMethod.views.exeInsert(cur,sql)
            ShareMethod.views.connClose(conn,cur) 
            return render_to_response('MIinsert.html')
    else:
        form = MonitorInfo()
        return render_to_response('MImessage.html',{'message':"添加成功"})
'''
def update(req):
    id=req.REQUEST.get('id',0)
    print(id)
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,"select * from server_monitor_info where sn="+id)
    ServerMonitorInfo_list = []
    for row in cur:
        ServerMonitorInfo_list.append({'id':row[0],'server_sn':row[1],'monitor_sn':row[2],'value':row[3],'mark':row[4],'frequency':row[5],'last_time':row[6],'status':row[7],'type':row[8]})
    print(ServerMonitorInfo_list)
    return render_to_response('SMIedit.html',{'ServerMonitorInfo_list':ServerMonitorInfo_list})
    

def modify(req):
    id=req.REQUEST.get('id',0)
    server_sn=req.REQUEST.get('server_sn',0)
    monitor_sn=req.REQUEST.get('monitor_sn',0)
    value=req.REQUEST.get('value',0)
    mark=req.REQUEST.get('mark','0')
    frequency=req.REQUEST.get('frequency',0)
    status=req.REQUEST.get('status',0)
    type=req.REQUEST.get('type',0)

    conn,cur=ShareMethod.views.connDB()
    sql="update server_monitor_info set server_sn="+server_sn+",monitor_sn="+monitor_sn+",value="+value+",mark='"+mark+"',frequency="+frequency+",status="+status+",type="+type+"  where sn="+id
    print(sql)
    ShareMethod.views.exeUpdate(cur,sql)
    ShareMethod.views.connClose(conn,cur) 
    return render_to_response('SMImessage.html',{'message':"修改成功"})
'''        
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
'''
def select(req):
    search=req.REQUEST.get('search','0')
    value=req.REQUEST.get('value','0')
    type=req.REQUEST.get('type','0')
    print(search)
    print(value)
    conn,cur=ShareMethod.views.connDB()
    sql= "select * from server_monitor_info where 1 =1 and type="+type
    if(search=='status'):
        sql += " and status = " + value 
    if(search=='type'):
        sql += " and type = " + value 
    ShareMethod.views.exeQuery(cur,sql) 
    ShareMethod.views.connClose(conn,cur) 
    contact_list = []
    for row in cur:
        contact_list.append({'id':row[0],'server_sn':row[1],'monitor_sn':row[2],'value':row[3],'mark':row[4],'frequency':row[5],'last_time':row[6],'status':row[7],'type':row[8]})
    content_list,page_range = ShareMethod.views.pagination(req, contact_list)
    print(content_list)
    return render_to_response('MIselect.html',{'ServerMonitorInfo_list':content_list,'page_range':page_range})
     
