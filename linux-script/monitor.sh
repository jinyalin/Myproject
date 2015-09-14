#!/bin/bash

dbPath="/var/log"
count=`find $dbPath -mmin -2 -name "mysqld.log" |wc -l`

monitor(){
message=`mysql -uroot -phstest2014 -e "use sms_client_new;select notice_content,status,email,mobile from system_notice_info where notice_module_sn=4;" | grep -v "notice_content"`
        content="$filePath"`echo $message | awk '{print $1}'`
        status=`echo $message | awk '{print $2}'`
        email=`echo $message | awk '{print $3}'`
        mobile=`echo $message | awk '{print $4}'`
        #邮件预警
        if [ $status -eq 2 ];then
           curl --data "account=guomei&passwd=gm1515&content=$content&email=$email&emailwarning=1"  http://124.127.184.89:8180/PlateWarning
        fi
        #不预警
        if [ $status -eq 0 ];then
           exit 0
        fi
        #短信预警
        if [ $status -eq 1 ];then
           curl --data "account=guomei&passwd=gm1515&content=$content&mobile=$mobile&smswarning=1"  http://124.127.184.89:8180/PlateWarning
        fi
        #短信及邮件预警
        if [ $status -eq 3 ];then
           curl --data "account=guomei&passwd=gm1515&content=$content&mobile=$mobile&smswarning=1&email=$email&emailwarning=1"  http://124.127.184.89:8180/PlateWarning
        fi
}

if [ $count -gt 0 ];then
   filePath="/var/log/mysqld.log"
   monitor
fi
