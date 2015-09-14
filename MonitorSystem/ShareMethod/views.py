from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger ,InvalidPage
import pymysql
import logging
import socket

if  socket.gethostname() == 'vm-ywcs03':
    filename_info="/hskj/web/apache/htdocs/MonitorSystem/info.log"
    filename_error="/hskj/web/apache/htdocs/MonitorSystem/error.log"
else:
    filename_info="E:\workspace\MonitorSystem\info.log"
    filename_error="E:\workspace\MonitorSystem\error.log"
   
def InfoLog(message):
    format='%(asctime)s - %(levelname)s - %(message)s'
    #curDate = datetime.date.today() - datetime.timedelta(days=0)
    ##dateTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    logging.basicConfig(filename=filename_info, level=logging.INFO , format=format)
    logging.info(message)
    
def ErrorLog(message):
    format='%(asctime)s - %(pathname)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s'
    #curDate = datetime.date.today() - datetime.timedelta(days=0)
    logging.basicConfig(filename=filename_error, level=logging.ERROR , format=format)
    logging.error(message)
    
def connDB():
    if socket.gethostname() == 'vm-ywcs03':
        conn=  pymysql.connect(host='210.14.134.77',port=13306,user='notice_plate',passwd='hskj&U*I(O1207',db='monitor',charset='utf8')
    else:
        conn=  pymysql.connect(host='192.168.120.12',user='root',passwd='123456',db='monitor_server',charset='utf8')
    cur = conn.cursor()
    return (conn,cur)

def connDB1():
    if socket.gethostname() == 'vm-ywcs03':
        conn=  pymysql.connect(host='210.14.134.77',port=13306,user='notice_plate',passwd='hskj&U*I(O1207',db='super_plate',charset='utf8')
    else:
        conn=  pymysql.connect(host='192.168.120.12',user='root',passwd='123456',db='monitor_server',charset='utf8')
    cur = conn.cursor()
    return (conn,cur)
def connDB2():
    if socket.gethostname() == 'vm-ywcs03':
        conn=  pymysql.connect(host='210.14.134.77',port=13306,user='notice_plate',passwd='hskj&U*I(O1207',db='remote_bak_server',charset='utf8')
    else:
        conn=  pymysql.connect(host='192.168.120.12',user='root',passwd='123456',db='monitor_server',charset='utf8')
    cur = conn.cursor()
    return (conn,cur)

def exeQuery(cur,sql):
    cur.execute(sql)
    return(cur)
def exeUpdate(cur,sql):
    sta=cur.execute(sql)
    return (sta)
def exeDelete(cur,sql):
    sta = cur.execute(sql)
    return(sta)
def exeInsert(cur,sql):
    cur.execute(sql)
    return(cur)
def connClose(conn,cur):
    cur.close()
    conn.close()   
      
def pagination(sql,pageType,curPage,allPostCounts):  
    
    ONE_PAGE_OF_DATA = 10
    after_range_num = 5   
    befor_range_num = 4
    allPage = int(allPostCounts / ONE_PAGE_OF_DATA)
    remainPost = allPostCounts % ONE_PAGE_OF_DATA
    if remainPost > 0:
        allPage += 1
    print(allPage)  
    if curPage >= after_range_num:
        if curPage+after_range_num+1 > allPage:
            pageList = range(curPage-befor_range_num,allPage+1)
        else:
            pageList = range(curPage-befor_range_num,curPage+after_range_num+1)
    else:
        if after_range_num+1 > allPage:
            pageList = range(1,allPage+1)
        else:
            pageList = range(1,curPage+after_range_num+1)
            
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
        
    startPos = (curPage-1)*ONE_PAGE_OF_DATA
    print(startPos)
    table_list = [] 
    sql += " limit "+str(startPos)+","+str(ONE_PAGE_OF_DATA)
    print(sql)
    return table_list,allPage,curPage,allPostCounts,pageList,sql
    

def index(req):
    username = req.session.get('username','未登录')
    if username == "未登录":
        return HttpResponseRedirect('login')       
    return render_to_response('index.html',{'username':username})

def SuccessMessage(req):
    message=req.REQUEST.get("message")
    return render_to_response('SuccessMessage.html',{'message':message})
def FailureMessage(req):
    message=req.REQUEST.get("message")
    return render_to_response('FailureMessage.html',{'message':message})
