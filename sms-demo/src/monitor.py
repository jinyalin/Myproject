#!/bin/bash
#部署时需要根据实际需求更改以下变量。
#发送端日志路径
sendPath="/hskj/send"
#处理端日志路径
dealPath="/hskj/dealdata"
#可以查询数据库的账号及密码
mysql_query="mysql -uyunwei -pmobile707"
#短信和邮箱预警调用URL地址
monitor_url="http://yj.baiwutong.com:8180/PlateWarning"
#接收端tomcat启动的端口
plate_port="9998"

monitor(){
message=`$mysql_query -e "use sms_client_new;select notice_content,status,email,mobile from system_notice_info where notice_module_sn=$1;" | grep -v "notice_content"`
        content="$2 "`echo $message | awk '{print $1}'`
        status=`echo $message | awk '{print $2}'`
        email=`echo $message | awk '{print $3}'`
        mobile=`echo $message | awk '{print $4}'`
        #邮件预警
        if [ $status -eq 2 ];then
           curl --data "account=guomei&passwd=gm1515&content=$content&email=$email&emailwarning=1"  $monitor_url
        fi
        #不预警
        if [ $status -eq 0 ];then
           exit 0
        fi
        #短信预警
        if [ $status -eq 1 ];then
           curl --data "account=guomei&passwd=gm1515&content=$content&mobile=$mobile&smswarning=1"  $monitor_url
        fi
        #短信及邮件预警
        if [ $status -eq 3 ];then
           curl --data "account=guomei&passwd=gm1515&content=$content&mobile=$mobile&smswarning=1&email=$email&emailwarning=1"  $monitor_url
        fi
}
#账户余额不足监控
chargeFail=`$mysql_query -e "use sms_client_new;select customer_id,customer_name from customer_info where status=0 and sms_count=0;" | grep -v "customer_id"| awk '{print "账号："$1,"账户名称："$2}'`
if [  -n "$chargeFail" ];then
    result=$chargeFail
    monitor 9 "$result"
fi

#端口监控
PortListen=`netstat -an | grep -a "$plate_port" | grep -a "LISTEN" | wc -l`
if [ $PortListen != 1 ];then
    monitor 6 ''
fi
#发送端日志通道异常监控
td_socket_fail=`tail -200 $sendPath/log/info.log | egrep -a "socket to ip.*failure" |awk '{print $6,$7,$8,$9,$10,$11}' | sort | uniq`
td_login_fail=`tail -200 $sendPath/log/info.log |grep -a "loginResp:"| grep -v "loginResp:0" | awk  '{print $(NF-3),$NF}' | sort |uniq`
td_submit_fail=`tail -200 $sendPath/log/info.log |grep -a "submitResp:"| grep -v "submitResp:0" | awk  '{print $(NF-3),$NF}' | sort |uniq`
if [  -n "$td_socket_fail" ];then
    result=$td_socket_fail
    monitor 1 "$result"
fi
if [  -n "$td_login_fail" ];then
    result=$td_login_fail
    monitor 1 "$result"
fi
if [  -n "$td_submit_fail" ];then
    result=$td_submit_fail
    monitor 1 "$result"
fi
#待发送数据表监控
SendStack=`$mysql_query -e "use sms_client_new;select count(*) as amount,td_code from sms_send_info where status=100 and timestampdiff(minute,update_time,now()) >2 group by 2;" | grep -v "amount" | awk '$1>0{print $0}' |grep -v "^$"`
if [  -n "$SendStack" ];then
    td_code=`echo $SendStack|awk '{print $2}'`
    count=`echo $SendStack|awk '{print $1}'`
    result="通道代码：$td_code,积压2分钟前100状态的信息数量:$count "
    monitor 5 "$result"
fi
#发送端和处理端程序日志异常监控
count_send_dao=`find $sendPath/log -mmin -2 -name "dao.log" |wc -l`
count_send_err=`find $sendPath/log -mmin -2 -name "error.log" |wc -l`
count_deal_dao=`find $dealPath/log -mmin -2 -name "dao.log" |wc -l`
count_deal_err=`find $dealPath/log -mmin -2 -name "error.log" |wc -l`
if [ $count_send_dao -gt 0 ];then
   result="$sendPath/log/dao.log "
   monitor 3 $result
fi
if [ $count_send_err -gt 0 ];then
   result="$sendPath/log/error.log "
   monitor 3 $result
fi
if [ $count_deal_dao -gt 0 ];then
   result="$dealPath/log/dao.log "
   monitor 3 $result
fi
if [ $count_deal_err -gt 0 ];then
    result="$dealPath/log/error.log "
    monitor 3 $result
fi
#磁盘空间监控
DISK_USED=`df -h |grep -v /dev/mapper/ |grep -v "Filesystem"|grep -v "文件系统"|awk '{print $(NF-1)}'|awk -F'%' '{print $1}' | xargs`
for i in $DISK_USED
do
  if [ "$i" -ge 70 ];then
    monitor 4 ''
    fi
done
#进程监控
process=( "sms_send_kit_send"   "sms_send_kit_dealdata"  "tomcat_client"  "mysqld_safe"  "/usr/libexec/mysqld")
for i in ${process[*]}
do
    PID=$i
    PID_COUNT=`ps -ef|grep "$PID"|grep -v grep|wc -l`

    if [ $PID_COUNT -lt 1 ];then
        result=$PID
        monitor 2 $result
    fi
done
