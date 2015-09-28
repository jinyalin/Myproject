from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger ,InvalidPage
import pymysql

def connDB():
    conn=  pymysql.connect(host='localhost',user='root',passwd='123456',db='monitor_server',charset='utf8')
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
      
def pagination(req,list):      
    after_range_num = 5   
    befor_range_num = 4      
    try:                     
        page = int(req.GET.get("page",1)) 
        if page < 1: 
            page = 1 
    except ValueError: 
            page = 1 
    paginator = Paginator(list,10)
    try:                     
        content_list = paginator.page(page) 
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        content_list = paginator.page(paginator.num_pages)
    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+befor_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+befor_range_num]
    print(content_list)
    return(content_list,page_range)   