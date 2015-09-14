from django.template.loader import get_template
from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
import ShareMethod.views


def select_mt(req,sql,sql2,sql3,html):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    flag='0'
    search=req.REQUEST.get('search',0)
    value=req.REQUEST.get('value',0)
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')
    conn,cur=ShareMethod.views.connDB_auto()

    if(search=='td_code'):
        sql += " and td_code like '%" + value + "%'"
        sql2 += " and td_code like '%" + value + "%'"
        sql3 += " and td_code like '%" + value + "%'"

    if startTime!=endTime:
        if startTime!='':
            sql +=" and insert_time >='"+startTime+"'"
            sql2 +=" and insert_time >='"+startTime+"'"
            sql3 +=" and insert_time >='"+startTime+"'"
        if endTime!='':
            sql +=" and insert_time <='"+endTime+"'"
            sql2 +=" and insert_time <='"+endTime+"'"
            sql3 +=" and insert_time <='"+endTime+"'"
    else:
        if startTime!='':
            sql +=" and insert_time like '%"+startTime+"%'"
            sql2 +=" and insert_time like '%"+startTime+"%'"            
            sql3 +=" and insert_time like '%"+startTime+"%'"            
    sql += "  group by td_code,province,mobile "
    sql2 += "  group by td_code,province,mobile) c"
    sql3 += "  group by td_code,province,mobile) d)"
    sql += "  order by fail_describe desc "
    print(sql2)
    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB_auto()
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
        print(sql2)
        ShareMethod.views.connClose(conn2,cur2)
        
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    
    ShareMethod.views.exeQuery(cur,sql) 
    table_list = []
    table_flist = []
    province=""
    for row in cur:
        table_list.append({'td_code':row[0],'province':row[1],'mobile':row[2],'fail_describe':row[3],'amount':row[4]})
    if(search=='td_code' and value!=''):
        flag='1'
        ShareMethod.views.exeQuery(cur,sql3)
        for row in cur:
            table_flist.append({'td_code':value,'province':row[0],'mobile':row[1]}) 
    ShareMethod.views.connClose(conn,cur) 
    return render_to_response(html,locals())

def selectMt_un(req):
    html="TSselectMt_un.html"
    sql= "select b.td_code,a.province,b.mobile,b.fail_describe,count(*) as amount from provinces_test_un.phone_card a ,receive_report_info b  where a.mobile=b.mobile "
    sql2="select count(*) from (select b.td_code,a.province,b.mobile,count(*) as amount from provinces_test_un.phone_card a ,receive_report_info b  where a.mobile=b.mobile "
    sql3="select province,mobile from provinces_test_un.phone_card where mobile not in (select mobile from (select b.td_code,a.province,b.mobile,b.fail_describe,count(*) as amount from provinces_test_un.phone_card a ,receive_report_info b  where a.mobile=b.mobile "
    return select_mt(req,sql,sql2,sql3,html)
def selectMt_cm(req):
    html="TSselectMt_cm.html"
    sql= "select b.td_code,a.province,b.mobile,b.fail_describe,count(*) as amount from provinces_test_cm.phone_card a ,receive_report_info b  where a.mobile=b.mobile "
    sql2="select count(*) from (select b.td_code,a.province,b.mobile,count(*) as amount from provinces_test_cm.phone_card a ,receive_report_info b  where a.mobile=b.mobile "
    sql3="select province,mobile from provinces_test_cm.phone_card where mobile not in (select mobile from (select b.td_code,a.province,b.mobile,b.fail_describe,count(*) as amount from provinces_test_cm.phone_card a ,receive_report_info b  where a.mobile=b.mobile "
    return select_mt(req,sql,sql2,sql3,html)
def selectMt_cdma(req):
    html="TSselectMt_cdma.html"
    sql= "select b.td_code,a.province,b.mobile,b.fail_describe,count(*) as amount from provinces_test_cdma.phone_card a ,receive_report_info b  where a.mobile=b.mobile "
    sql2="select count(*) from (select b.td_code,a.province,b.mobile,count(*) as amount from provinces_test_cdma.phone_card a ,receive_report_info b  where a.mobile=b.mobile "
    sql3="select province,mobile from provinces_test_cdma.phone_card where mobile not in (select mobile from (select b.td_code,a.province,b.mobile,b.fail_describe,count(*) as amount from provinces_test_cdma.phone_card a ,receive_report_info b  where a.mobile=b.mobile "
    return select_mt(req,sql,sql2,sql3,html)
def selectMt_cdma1(req):
    html="TSselectMt_cdma1.html"
    sql= "select b.td_code,a.province,b.mobile,b.fail_describe,count(*) as amount from provinces_test_cdma1.phone_card a ,receive_report_info b  where a.mobile=b.mobile "
    sql2="select count(*) from (select b.td_code,a.province,b.mobile,count(*) as amount from provinces_test_cdma1.phone_card a ,receive_report_info b  where a.mobile=b.mobile "
    sql3="select province,mobile from provinces_test_cdma1.phone_card where mobile not in (select mobile from (select b.td_code,a.province,b.mobile,b.fail_describe,count(*) as amount from provinces_test_cdma1.phone_card a ,receive_report_info b  where a.mobile=b.mobile "
    return select_mt(req,sql,sql2,sql3,html)


def select_mo(req,sql,sql2,sql3,html):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    
    flag='0'
    search=req.REQUEST.get('search',0)
    value=req.REQUEST.get('value',0)
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')
    conn,cur=ShareMethod.views.connDB_auto()

    if(search=='dest_mobile'):
        sql += " and dest_mobile like '%" + value + "%'"
        sql2 += " and dest_mobile like '%" + value + "%'"
        sql3 += " and dest_mobile like '%" + value + "%'"

    if startTime!=endTime:
        if startTime!='':
            sql +=" and insert_time >='"+startTime+"'"
            sql2 +=" and insert_time >='"+startTime+"'"
            sql3 +=" and insert_time >='"+startTime+"'"
        if endTime!='':
            sql +=" and insert_time <='"+endTime+"'"
            sql2 +=" and insert_time <='"+endTime+"'"
            sql3 +=" and insert_time <='"+endTime+"'"
    else:
        if startTime!='':
            sql +=" and insert_time like '%"+startTime+"%'"
            sql2 +=" and insert_time like '%"+startTime+"%'"            
            sql3 +=" and insert_time like '%"+startTime+"%'"            
    sql += "  group by dest_mobile,province,src_terminal_id "
    sql2 += "  group by dest_mobile,province,src_terminal_id) c"
    sql3 += "  group by dest_mobile,province,src_terminal_id) d)"
    print(sql2)
    if allPostCounts == 0:
        conn2,cur2=ShareMethod.views.connDB_auto()
        ShareMethod.views.exeQuery(cur2,sql2)
        for row in cur2:
            allPostCounts = row[0]
        print(sql2)
        ShareMethod.views.connClose(conn2,cur2)
        
    table_list,allPage,curPage,allPostCounts,pageList,sql = ShareMethod.views.pagination(sql, pageType, curPage, allPostCounts)
    
    ShareMethod.views.exeQuery(cur,sql) 
    table_list = []
    table_flist = []
    province=""
    for row in cur:
        table_list.append({'dest_mobile':row[0],'province':row[1],'mobile':row[2],'msg_content':row[3],'amount':row[4]})
    if(search=='dest_mobile' and value!=''):
        flag='1'
        ShareMethod.views.exeQuery(cur,sql3)
        for row in cur:
            table_flist.append({'dest_mobile':value,'province':row[0],'mobile':row[1]}) 
    ShareMethod.views.connClose(conn,cur) 
    return render_to_response(html,locals())



def selectMo_un(req):
    html="TSselectMo_un.html"
    sql= "select b.dest_mobile,a.province,b.src_terminal_id,b.msg_content,count(*) as amount from provinces_test_un.phone_card a ,deliver_sms_info b  where a.mobile=b.src_terminal_id "
    sql2="select count(*) from (select b.dest_mobile,a.province,b.src_terminal_id,b.msg_content,count(*) as amount from provinces_test_un.phone_card a ,deliver_sms_info b  where a.mobile=b.src_terminal_id "
    sql3="select province,mobile from  provinces_test_un.phone_card  where mobile not in (select src_terminal_id from ( select b.dest_mobile,a.province,b.src_terminal_id,b.msg_content,count(*) as amount from provinces_test_un.phone_card a ,deliver_sms_info b  where a.mobile=b.src_terminal_id  "
    return select_mo(req,sql,sql2,sql3,html)
def selectMo_cm(req):
    html="TSselectMo_cm.html"
    sql= "select b.dest_mobile,a.province,b.src_terminal_id,b.msg_content,count(*) as amount from provinces_test_cm.phone_card a ,deliver_sms_info b  where a.mobile=b.src_terminal_id "
    sql2="select count(*) from (select b.dest_mobile,a.province,b.src_terminal_id,b.msg_content,count(*) as amount from provinces_test_cm.phone_card a ,deliver_sms_info b  where a.mobile=b.src_terminal_id "
    sql3="select province,mobile from  provinces_test_cm.phone_card  where mobile not in (select src_terminal_id from ( select b.dest_mobile,a.province,b.src_terminal_id,b.msg_content,count(*) as amount from provinces_test_cm.phone_card a ,deliver_sms_info b  where a.mobile=b.src_terminal_id  "
    return select_mo(req,sql,sql2,sql3,html)
def selectMo_cdma(req):
    html="TSselectMo_cdma.html"
    sql= "select b.dest_mobile,a.province,b.src_terminal_id,b.msg_content,count(*) as amount from provinces_test_cdma.phone_card a ,deliver_sms_info b  where a.mobile=b.src_terminal_id "
    sql2="select count(*) from (select b.dest_mobile,a.province,b.src_terminal_id,b.msg_content,count(*) as amount from provinces_test_cdma.phone_card a ,deliver_sms_info b  where a.mobile=b.src_terminal_id "
    sql3="select province,mobile from  provinces_test_cdma.phone_card  where mobile not in (select src_terminal_id from ( select b.dest_mobile,a.province,b.src_terminal_id,b.msg_content,count(*) as amount from provinces_test_cdma.phone_card a ,deliver_sms_info b  where a.mobile=b.src_terminal_id  "
    return select_mo(req,sql,sql2,sql3,html)
def selectMo_cdma1(req):
    html="TSselectMo_cdma1.html"
    sql= "select b.dest_mobile,a.province,b.src_terminal_id,b.msg_content,count(*) as amount from provinces_test_cdma1.phone_card a ,deliver_sms_info b  where a.mobile=b.src_terminal_id "
    sql2="select count(*) from (select b.dest_mobile,a.province,b.src_terminal_id,b.msg_content,count(*) as amount from provinces_test_cdma1.phone_card a ,deliver_sms_info b  where a.mobile=b.src_terminal_id "
    sql3="select province,mobile from  provinces_test_cdma1.phone_card  where mobile not in (select src_terminal_id from ( select b.dest_mobile,a.province,b.src_terminal_id,b.msg_content,count(*) as amount from provinces_test_cdma1.phone_card a ,deliver_sms_info b  where a.mobile=b.src_terminal_id  "
    return select_mo(req,sql,sql2,sql3,html)