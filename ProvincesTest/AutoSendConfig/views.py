from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
import ShareMethod.views
import time
def insert(req):
        operatorName=req.session.get('username')
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        if req.method == 'POST':
            
            thread_name=req.REQUEST.get('thread_name','0')
            thread_param=req.REQUEST.get('thread_param','0')
            app_name=req.REQUEST.get('app_name','0')
            sql=""
            status=req.REQUEST.get('status','0')
            sql2="select max(thread_id) from thread_controller"
            try:
                conn,cur=ShareMethod.views.connDB_auto()
                conn2,cur2=ShareMethod.views.connDB_auto()
                print(sql)
                ShareMethod.views.exeQuery(cur2,sql2)
                for row in cur2:
                    thread_id=int(row[0])+1
                sql="insert into thread_controller(thread_name,thread_id,status,thread_param,thread_type,group_id,app_name) values ('"+thread_name+"'," + str(thread_id) +","+str(4)+",'"+thread_param+"',"+str(1)+","+str(0)+",'"+app_name+"')"
                SqlResult=ShareMethod.views.exeInsert(cur,sql)
                print(SqlResult)
                ShareMethod.views.connClose(conn,cur)
                ShareMethod.views.connClose(conn2,cur2)
            except Exception as e:
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message=AutoSendConfig/insert.do')
            ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
            return HttpResponseRedirect('../SuccessMessage.do?message=AutoSendConfig/insert.do')
        else:
            return render_to_response('ASCinsert.html')


def update(req):
    id=req.REQUEST.get('id',0)
    print(id)
    conn,cur=ShareMethod.views.connDB_auto()
    ShareMethod.views.exeQuery(cur,"select sn,thread_name,thread_param,app_name,status,thread_type from thread_controller where sn="+str(id))
    ShareMethod.views.connClose(conn,cur)
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'thread_name':row[1],'thread_param':row[2],'app_name':row[3],'status':row[4],'thread_type':row[5]})
    print(table_list)
    return render_to_response('ASCedit.html',{'table_list':table_list})
    

def modify(req):
    operatorName=req.session.get('username')
    id=req.REQUEST.get('id',0)
    thread_name=req.REQUEST.get('thread_name','0')
    thread_param=req.REQUEST.get('thread_param','0')
    app_name=req.REQUEST.get('app_name','0')
    status=req.REQUEST.get('status','0')
    thread_type=req.REQUEST.get('thread_type','0')
    print("---------------------"+status)
    sql=""
    if thread_type == '1':
        if status == '6':
            sql="update thread_controller set thread_name='"+thread_name+"',thread_param='"+thread_param+"',app_name='"+app_name + "',status=4  where sn="+id
        else:
            sql="update thread_controller set thread_name='"+thread_name+"',thread_param='"+thread_param+"',app_name='"+app_name + "'  where sn="+id
    else:
        if status == '3':
            sql="update thread_controller set thread_name='"+thread_name+"',thread_param='"+thread_param+"',app_name='"+app_name + "',status=1,thread_type=1  where sn="+id   
        else:
            sql="update thread_controller set thread_name='"+thread_name+"',thread_param='"+thread_param+"',app_name='"+app_name + "'  where sn="+id
        
    try:
        conn,cur=ShareMethod.views.connDB_auto()
        print(sql)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur) 
    except Exception as e:
        print(e)
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=AutoSendConfig/select.do')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=AutoSendConfig/select.do') 
        
def select(req):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    search=req.REQUEST.get('search',0)
    value=req.REQUEST.get('value',0)
    conn,cur=ShareMethod.views.connDB_auto()
    sql= "select * from thread_controller where 1 =1 "
    sql2="select count(*) from thread_controller where 1=1 "
    if(search=='thread_param'):
        sql += " and thread_param like '%" + value + "%'"
        sql2 += " and thread_param like '%" + value + "%'"
    sql += " order by status asc"
    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB_auto()
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
        print(sql2)
        ShareMethod.views.connClose(conn2,cur2)
        
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    
    ShareMethod.views.exeQuery(cur,sql) 
    ShareMethod.views.connClose(conn,cur) 
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'thread_name':row[1],'thread_id':row[2],'status':row[3],'thread_param':row[4],'thread_type':row[5],'group_id':row[6],'app_name':row[7]})
    return render_to_response('ASCselect.html',locals())
