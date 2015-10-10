#! /bin/bash

content=`mysql -uyunwei -pmobile707 -e "use monitor;select content  from  notice_info where content like '%通道%失败率%' and insert_time > DATE_ADD(now(),INTERVAL -5 MINUTE) and alarm_type='sms' and content like '%集群%' limit 1;" | grep -v "content" ` 
if [ "$content" != "" ];then
ip='172.16.10.89'
yw_code=`echo "$content"| awk -F [：,]+ '{print $2}'`
server_name="集群服务器"
content1=`mysql -uremote_query -p20141024 -h$ip -e "use cluster_server;select response,err,fail_desc,count(*) from submit_message_send_history where td_code = \"$yw_code\" and insert_time > DATE_ADD(now(),INTERVAL -20 MINUTE) group by 1,2,3 order by 4 desc limit 3;" | xargs` && curl --data "account=yunwei&passwd=123&emailwarning=1&email=yunwei@baiwutong.com&smswarning=1&mobile=13311030239,13261289750,15321906869&content=$server_name通道：$yw_code，失败原因：$content1" http://yj.baiwutong.com:8180/PlateWarning
fi





