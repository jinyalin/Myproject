from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
import ShareMethod.views

class NoticeType(forms.Form):
    type = forms.IntegerField()
    type_desc = forms.CharField()
    mobiles = forms.CharField()

def insert(req):
    if req.method == 'POST':
        form = NoticeType(req.POST)
        if form.is_valid():
            type=form.cleaned_data['type']
            type_desc=form.cleaned_data['type_desc']
            mobiles=form.cleaned_data['mobiles']
            conn,cur=ShareMethod.views.connDB()
            sql="insert into notice_type(type,type_desc,mobiles,insert_time) values ("+type+",'" + type_desc +"','"+mobiles+"',now())"
            print(sql)
            ShareMethod.views.exeInsert(cur,sql)
            ShareMethod.views.connClose(conn,cur)
            return render_to_response('NTmessage.html',{'message':"插入成功"}) 
            
    else:
        form = NoticeType()
        return render_to_response('NTinsert.html')

def update(req):
    id=req.REQUEST.get('id',0)
    print(id)
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,"select * from notice_type where sn="+id)
    mobiles_list = []
    for row in cur:
        mobiles_list.append({'id':row[0],'type':row[1],'type_desc':row[2],'mobiles':row[3],'insert_time':row[4]})
    print(mobiles_list)
    #result = "{'id':row[0],'type':row[1],'type_desc':row[2],'mobiles':row[3],'insert_time':row[4]}";
    return render_to_response('NTedit.html',{'mobiles_list':mobiles_list})
    #return render_to_response('edit.html',{'model':result})
    

def modify(req):
    id=req.REQUEST.get('id',0)
    type=req.REQUEST.get('type',0)
    type_desc=req.REQUEST.get('type_desc','0')
    mobiles=req.REQUEST.get('mobiles','0')
    #print(id)
    conn,cur=ShareMethod.views.connDB()
    sql="update notice_type set type="+type+",type_desc='"+type_desc+"',mobiles='"+mobiles+"'  where sn="+id
    print(sql)
    ShareMethod.views.exeUpdate(cur,sql)
    ShareMethod.views.connClose(conn,cur) 
    return render_to_response('NTmessage.html',{'message':"修改成功"})
        
def delete(req): 
    id=req.REQUEST.get('id',0)
    print(type(id))
    print(id)
    conn,cur=ShareMethod.views.connDB()
    sql="delete from notice_type where sn="+id
    print(sql)
    ShareMethod.views.exeDelete(cur,sql)
    ShareMethod.views.connClose(conn,cur)
    return render_to_response('NTmessage.html',{'message':"删除成功"})

def select(req):
    search=req.REQUEST.get('search',0)
    value=req.REQUEST.get('value',0)
    conn,cur=ShareMethod.views.connDB()
    sql= "select * from notice_type where 1 =1 "
    if(search=='type'):
        sql += " and type = '" + value + "'"
    if(search=='type_desc'):
        sql += " and type_desc like '%" + value + "%'"
    if(search=='mobiles'):
        sql += " and mobiles like '%" + value + "%'"
    ShareMethod.views.exeQuery(cur,sql) 
    ShareMethod.views.connClose(conn,cur) 
    contact_list = []
    for row in cur:
        contact_list.append({'id':row[0],'type':row[1],'type_desc':row[2],'mobiles':row[3],'insert_time':row[4]})
    content_list,page_range = ShareMethod.views.pagination(req, contact_list)
    return render_to_response('NTselect.html',{'mobiles_list':content_list,'page_range':page_range})
     


    