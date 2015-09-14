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
            server_all_check=req.POST.getlist('ServerName','0')
            group_sn=req.REQUEST.get('groupName')
            delimiter = ','
            server_sn=delimiter.join(server_all_check)
            print(group_sn)
            print(server_sn)
            sql="insert into server_manager(group_sn,server_sn,insert_time) values ('"+group_sn+"','" + server_sn +"','"+NowTime+"')"
            try:
                conn,cur=ShareMethod.views.connDB()
                print(sql)
                SqlResult=ShareMethod.views.exeInsert(cur,sql)
                print(SqlResult)
                ShareMethod.views.connClose(conn,cur)
            except Exception as e:
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message=ServerManager/insert.do')
            
            ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
            return HttpResponseRedirect('../SuccessMessage.do?message=ServerManager/insert.do')
        else:
            
            conn1,cur1=ShareMethod.views.connDB()
            conn2,cur2=ShareMethod.views.connDB() 
            sql1="select server_name,sn from server_info order by server_name"  
            sql2="select group_name,sn from user_group" 
            ShareMethod.views.exeQuery(cur1,sql1)
            ShareMethod.views.exeQuery(cur2,sql2)
            ShareMethod.views.connClose(conn1,cur1)
            ShareMethod.views.connClose(conn2,cur2)
            serverNames=[]
            groupNames=[]
            for row1 in cur1:
                serverNames.append({'serverName':row1[0],'serverSn':row1[1]})
            for row2 in cur2:
                groupNames.append({'groupName':row2[0],'groupSn':row2[1]})
            print(serverNames)
            print(groupNames)
            return render_to_response('SMinsert.html',{'serverNames':serverNames,'groupNames':groupNames})


def update(req):
    id=req.REQUEST.get('id',0)
    print(id)
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,"select sn,group_sn,server_sn,agent_sn from server_manager where sn="+str(id))
    ShareMethod.views.connClose(conn,cur) 
    conn1,cur1=ShareMethod.views.connDB()
    conn2,cur2=ShareMethod.views.connDB()
    sql="select server_name,sn from server_info"  
    sql2="select group_name,sn from user_group"
    ShareMethod.views.exeQuery(cur1,sql)
    ShareMethod.views.exeQuery(cur2,sql2)
    ShareMethod.views.connClose(conn1,cur1)
    ShareMethod.views.connClose(conn2,cur2)
    ServerNames=[]
    GroupNames=[]
    for row in cur2:
        GroupNames.append({'groupName':row[0],'groupSn':str(row[1])})
    for row in cur1:
        ServerNames.append({'serverName':row[0],'serverSn':str(row[1])})
    print(GroupNames)
    table_list = []
    for row in cur:
        table_list.append({'id':row[0],'group_sn':row[1],'server_sn':row[2].split(','),'agent_sn':row[3]})
    print(table_list)
    return render_to_response('SMedit.html',{'table_list':table_list,'ServerNames':ServerNames,'GroupNames':GroupNames})
    

def modify(req):
    group_sn=req.REQUEST.get('groupName','0')
    agent_sn=req.REQUEST.get('agentName','0')
    print(group_sn)
    user_all_check=req.POST.getlist('ServerName','0')
    delimiter = ','
    server_sn=delimiter.join(user_all_check)
    operatorName=req.session.get('username')
    id=req.REQUEST.get('id',0)
    try:
        conn,cur=ShareMethod.views.connDB()
        sql="update server_manager set group_sn='"+group_sn+"',server_sn='"+server_sn+"',agent_sn='"+agent_sn+"' where sn="+str(id)
        print(sql)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur) 
    except Exception as e:
        print(e)
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=ServerManager/select.do')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=ServerManager/select.do') 

def delete(req): 
    operatorName=req.session.get('username')
    id=req.REQUEST.get('id',0)
    try:
        conn,cur=ShareMethod.views.connDB()
        sql="delete from server_manager where sn="+id
        print(sql)
        ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur) 
    except Exception as e:
        print(e)
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=ServerManager/select.do')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=ServerManager/select.do') 

def select(req):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    type=req.REQUEST.get('type','0')
    conn,cur=ShareMethod.views.connDB()
    sql= "select * from server_manager where 1 =1 order by group_mark"
    sql2 = "select count(*) from server_manager where 1=1 "
    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB()
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
        ShareMethod.views.connClose(conn2,cur2)
        
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    
    ShareMethod.views.exeQuery(cur,sql) 
    ShareMethod.views.connClose(conn,cur) 
    table_list = []
    serverSn_list = []
    conn3,cur3=ShareMethod.views.connDB()
    conn4,cur4=ShareMethod.views.connDB()
    conn5,cur5=ShareMethod.views.connDB()
    for row in cur:
        serverName_list =[]
        serverRoom_list =[]
        sql4="select group_name from user_group where sn ="+str(row[2])
        sql5="select group_name from user_group where sn="+str(row[5])
        ShareMethod.views.exeQuery(cur4,sql4)
        ShareMethod.views.exeQuery(cur5,sql5)
        for row4 in cur4:
            group_name=row4[0]
        for row5 in cur5:
            agent_name=row5[0]
        serverSn_list = row[3].split(',')
        print(serverSn_list)
        for sn in serverSn_list:
            sql3="select server_name from server_info where sn ="+str(sn)
            ShareMethod.views.exeQuery(cur3,sql3)
            for name in cur3:
                serverName_list.append(name[0])
            delimiter = ' , '
            server_name = delimiter.join(serverName_list) 
        print(row)
        table_list.append({'id':row[0],'group_mark':row[1],'group_name':group_name,'server_name':server_name,'insert_time':row[4],'agent_name':agent_name,'server_room':row[6]})
    ShareMethod.views.connClose(conn3,cur3)
    ShareMethod.views.connClose(conn4,cur4)
    if type == '0':
        return render_to_response('SMselect.html',locals())
    else:
        return render_to_response('SMselect1.html',locals())
        