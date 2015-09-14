from django.template.loader import get_template
from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
import ShareMethod.views
from django.http.response import HttpResponseRedirect
import datetime,time
import os
import xlrd

class YysData(forms.Form):
    yys_file = forms.FileField(label='upload',widget=forms.FileInput(attrs={'size':'100'}), required = True)

def upload(req):
    if req.method == "POST":
        yf = YysData(req.POST,req.FILES)
        operatorName=req.session.get('username')
        start_time = datetime.date(datetime.date.today().year,datetime.date.today().month-1,1)
        end_time = datetime.date(datetime.date.today().year,datetime.date.today().month,1)-datetime.timedelta(1)
        last_month = os.popen("date -d 'last-month' +%Y-%m")
        be_area=req.REQUEST.get('be_area','0')
        be_type=req.REQUEST.get('be_type','0')
        mode=req.REQUEST.get('mode','0')
        every_month = last_month.read().strip()
        conn1,cur1=ShareMethod.views.connDB1()
        conn2,cur2=ShareMethod.views.connDB1()
        sql_area = "select tag from tag_info where sn="+be_area
        sql_type = "select tag from tag_info where sn="+be_type
        ShareMethod.views.exeQuery(cur1,sql_area)
        ShareMethod.views.exeQuery(cur2,sql_type)
        ShareMethod.views.connClose(conn1,cur1) 
        ShareMethod.views.connClose(conn2,cur2) 
        area_name=""
        type_name=""
        for row1 in cur1:
            area_name = row1[0]
        for row2 in cur2:
            type_name = row2[0]
        gate_name = area_name + type_name
        file_name = ""
        if yf.is_valid():
            yys_file = yf.cleaned_data['yys_file']
            print(yys_file)
            print(yf.cleaned_data['yys_file'].name)
            print(yf.cleaned_data['yys_file'].size)
            file_name = "/upload/"+yf.cleaned_data['yys_file'].name
            fp = open(file_name,'wb')
            s = yf.cleaned_data['yys_file'].read()
            fp.write(s)
            fp.close()
        data = xlrd.open_workbook(file_name)
        #table = data.sheet_by_name(u'Sheet1')
        table = data.sheet_by_index(0)
        nrows = table.nrows
        ncols = table.ncols
        print("ncols:"+str(ncols))
        total = '0'
        user_name = ''
        sp_number=""
        success_count = '0'
        for i in range(1,nrows):
            if ncols >= 4:
                sp_number1 = str(table.cell(i,0).value)
                sp_number = sp_number1.split('.')[0]
                success_count = str(table.cell(i,1).value)
                print("success_count:"+str(success_count))
                total = str(table.cell(i,2).value)
                user_name = str(table.cell(i,3).value)
            if ncols == 3:
                sp_number1 = str(table.cell(i,0).value)
                sp_number = sp_number1.split('.')[0]
                success_count = str(table.cell(i,1).value)
                total = str(table.cell(i,2).value)
            if ncols == 2:
                sp_number1 = str(table.cell(i,0).value)
                sp_number = sp_number1.split('.')[0]
                success_count = str(table.cell(i,1).value) 
            sql = "insert into yys_data_handle(sp_number,start_time,end_time,total,success_count,user_name,gate_name,every_month,mode,be_area,be_type) values ('"+sp_number+"','" + str(start_time) +"','"+str(end_time)+"','"+str(total)+"',"+str(success_count)+",'"+user_name+"','"+gate_name+"','"+str(every_month)+"',"+str(mode)+","+str(be_area)+","+str(be_type)+")"
            print(sql)
            try:
                conn,cur=ShareMethod.views.connDB()
                result=ShareMethod.views.exeInsert(cur,sql)
                ShareMethod.views.connClose(conn,cur) 
            except Exception as e:
                ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
                return HttpResponseRedirect('../FailureMessage.do?message=YysBill/upload.do')
        ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
        return HttpResponseRedirect('../SuccessMessage.do?message=YysBill/upload.do')
    else:
        yf = YysData()
        conn1,cur1=ShareMethod.views.connDB1()
        conn2,cur2=ShareMethod.views.connDB1()
        sql_area = "select sn,tag from tag_info where type = 1"
        sql_type = "select sn,tag from tag_info where type = 2"
        ShareMethod.views.exeQuery(cur1,sql_area)
        ShareMethod.views.exeQuery(cur2,sql_type)
        ShareMethod.views.connClose(conn1,cur1) 
        ShareMethod.views.connClose(conn2,cur2) 
        be_areaList = []
        be_typeList = []
        for row1 in cur1:
            be_areaList.append({'sn':row1[0],'tag':row1[1]})
        for row2 in cur2:
            be_typeList.append({'sn':row2[0],'tag':row2[1]})
    return render_to_response('yys_upload.html',locals())


def insert(req):
    operatorName=req.session.get('username')
    start_time = datetime.date(datetime.date.today().year,datetime.date.today().month-1,1)
    end_time = datetime.date(datetime.date.today().year,datetime.date.today().month,1)-datetime.timedelta(1)
    last_month = os.popen("date -d 'last-month' +%Y-%m")
    every_month = last_month.read().strip()
    NowTime = time.strftime('%Y-%m-%d %H:%M:%S')
    be_area=req.REQUEST.get('be_area','0')
    be_type=req.REQUEST.get('be_type','0')
    mode=req.REQUEST.get('mode','0')
    sp_number=req.REQUEST.get('sp_number','0')
    success_count=req.REQUEST.get('success_count','0')
    total=req.REQUEST.get('total','0')
    user_name=req.REQUEST.get('user_name','0')
    conn1,cur1=ShareMethod.views.connDB1()
    conn2,cur2=ShareMethod.views.connDB1()
    sql_area = "select tag from tag_info where sn="+be_area
    sql_type = "select tag from tag_info where sn="+be_type
    ShareMethod.views.exeQuery(cur1,sql_area)
    ShareMethod.views.exeQuery(cur2,sql_type)
    ShareMethod.views.connClose(conn1,cur1) 
    ShareMethod.views.connClose(conn2,cur2) 
    area_name=""
    type_name=""
    for row1 in cur1:
        area_name = row1[0]
    for row2 in cur2:
        type_name = row2[0]
    gate_name = area_name + type_name
    if req.method == 'POST':
        sql="insert into yys_data_handle(sp_number,start_time,end_time,total,success_count,user_name,gate_name,every_month,mode,be_area,be_type) values ('"+sp_number+"','" + str(start_time) +"','"+str(end_time)+"','"+str(total)+"',"+str(success_count)+",'"+user_name+"','"+gate_name+"','"+str(every_month)+"',"+str(mode)+","+str(be_area)+","+str(be_type)+")"
        print(sql)
        try:
            conn,cur=ShareMethod.views.connDB()
            result=ShareMethod.views.exeInsert(cur,sql)
            ShareMethod.views.connClose(conn,cur) 
        except Exception as e:
            ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
            return HttpResponseRedirect('../FailureMessage.do?message=YysBill/insert.do')
        ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
        return HttpResponseRedirect('../SuccessMessage.do?message=YysBill/insert.do')
    else:
        conn1,cur1=ShareMethod.views.connDB1()
        conn2,cur2=ShareMethod.views.connDB1()
        sql_area = "select sn,tag from tag_info where type = 1"
        sql_type = "select sn,tag from tag_info where type = 2"
        ShareMethod.views.exeQuery(cur1,sql_area)
        ShareMethod.views.exeQuery(cur2,sql_type)
        ShareMethod.views.connClose(conn1,cur1) 
        ShareMethod.views.connClose(conn2,cur2) 
        be_areaList = []
        be_typeList = []
        for row1 in cur1:
            be_areaList.append({'sn':row1[0],'tag':row1[1]})
        for row2 in cur2:
            be_typeList.append({'sn':row2[0],'tag':row2[1]})
        return render_to_response('yys_insert.html',locals())

def select(req):
    allPostCounts = int(req.REQUEST.get('allPostCounts','0'))
    pageType = req.REQUEST.get('pageType','0')
    curPage = int(req.REQUEST.get('curPage','1'))
    allPage = int(req.REQUEST.get('allPage','1'))
    last_month = os.popen("date -d 'last-month' +%Y-%m")
    every_month = last_month.read().strip()
    search=req.REQUEST.get('search','0')
    value=req.REQUEST.get('value','0')
    startTime=req.REQUEST.get('startTime','')
    endTime=req.REQUEST.get('endTime','')
    
    sql= "select sn,every_month,gate_name,sp_number,mode,success_count from yys_data_handle where 1 =1 "
    sql2 = "select count(*) as count from yys_data_handle where 1=1 "
    
    sql += " and every_month='"+str(every_month)+"' "
    sql2 += " and every_month='"+str(every_month)+"' "
    if(search=='gate_name'):
        sql += " and  gate_name like '%" + value + "%'"
        sql2 += " and gate_name like '%" + value + "%'"
    if(search=='sp_number'):
        sql += " and sp_number like '%" + value + "%'"
        sql2 += " and sp_number like '%" + value + "%'"
    
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
    ShareMethod.views.exeQuery(cur,sql) 
    for row in cur:
        table_list.append({'id':row[0],'every_month':row[1],'gate_name':row[2],'sp_number':row[3],'mode':row[4],'success_count':row[5]})
    ShareMethod.views.connClose(conn,cur)
    return render_to_response('yys_select.html',locals())

def update(req):
    id=req.REQUEST.get('id',0)
    print(id)
    conn,cur=ShareMethod.views.connDB()
    ShareMethod.views.exeQuery(cur,"select sn,every_month,be_area,be_type,sp_number,mode,success_count,total,user_name from yys_data_handle where sn="+id)
    ShareMethod.views.connClose(conn,cur) 
    conn1,cur1=ShareMethod.views.connDB1()
    conn2,cur2=ShareMethod.views.connDB1()
    sql_area = "select sn,tag from tag_info where type = 1"
    sql_type = "select sn,tag from tag_info where type = 2"
    ShareMethod.views.exeQuery(cur1,sql_area)
    ShareMethod.views.exeQuery(cur2,sql_type)
    ShareMethod.views.connClose(conn1,cur1) 
    ShareMethod.views.connClose(conn2,cur2) 
    be_areaList = []
    be_typeList = []
    for row1 in cur1:
        be_areaList.append({'sn':row1[0],'tag':row1[1]})
    for row2 in cur2:
        be_typeList.append({'sn':row2[0],'tag':row2[1]})
    table_list = []
    for row in cur:
        if row[8]:
            user_name=row[8]
        else:
            user_name=''
        table_list.append({'id':row[0],'every_month':row[1],'be_area':row[2],'be_type':row[3],'sp_number':row[4],'mode':row[5],'success_count':row[6],'total':row[7],'user_name':user_name})
    return render_to_response('yys_edit.html',locals())
        
    
def modify(req):
    id=req.REQUEST.get('id',0)
    operatorName=req.session.get('username')
    sp_number=req.REQUEST.get('sp_number',0)
    mode=req.REQUEST.get('mode',0)
    be_area=req.REQUEST.get('be_area','0')
    be_type=req.REQUEST.get('be_type','0')
    success_count=req.REQUEST.get('success_count',0)
    total=req.REQUEST.get('total',0)
    if total == '':
        total = 0
    user_name=req.REQUEST.get('user_name',0)
    conn1,cur1=ShareMethod.views.connDB1()
    conn2,cur2=ShareMethod.views.connDB1()
    sql_area = "select tag from tag_info where sn="+be_area
    sql_type = "select tag from tag_info where sn="+be_type
    ShareMethod.views.exeQuery(cur1,sql_area)
    ShareMethod.views.exeQuery(cur2,sql_type)
    ShareMethod.views.connClose(conn1,cur1) 
    ShareMethod.views.connClose(conn2,cur2) 
    area_name=""
    type_name=""
    for row1 in cur1:
        area_name = row1[0]
    for row2 in cur2:
        type_name = row2[0]
    gate_name = area_name + type_name
    sql="update yys_data_handle set gate_name='"+gate_name+"',sp_number='"+sp_number+"',mode="+str(mode)+",be_area="+str(be_area)+",be_type="+str(be_type)+",success_count="+str(success_count)+",total="+str(total)+",user_name='"+user_name+"' where sn="+str(id)
    print(sql)
    try:
        conn,cur=ShareMethod.views.connDB()
        result=ShareMethod.views.exeUpdate(cur,sql)
        ShareMethod.views.connClose(conn,cur) 
    except Exception as e:
        ShareMethod.views.ErrorLog(str(e)+"操作人："+operatorName)
        return HttpResponseRedirect('../FailureMessage.do?message=YysBill/select.do')
    ShareMethod.views.InfoLog(sql+"操作人："+operatorName)
    return HttpResponseRedirect('../SuccessMessage.do?message=YysBill/select.do')
