#! /bin/bash

content=`mysql -uyunwei -pmobile707 -e "use monitor;select content  from  notice_info where content like '%通道%失败率为%' and insert_time > DATE_ADD(now(),INTERVAL -5 MINUTE) and alarm_type='sms' and content not like '%集群%' limit 1;" | grep -v "content" ` 
if [ "$content" != "" ];then

ip=`echo "$content" | awk -F [\)\(" "]+ '{print $1}'`
yw_code=`echo "$content" | awk -F [\)\(" "]+ '{print $4}'`
server_name=`echo "$content" | awk -F [\)\(" "]+ '{print $2}'`
alarm_value=`mysql -uyunwei -pmobile707 -e "use monitor;select alarm_value  from  notice_info where content like '%通道%失败率为%' and insert_time > DATE_ADD(now(),INTERVAL -5 MINUTE) and alarm_type='sms' limit 1;" | grep -v "alarm_value"` 
	if [ "${server_name:0:4}" == "cmpp" ];then
	content1=`mysql -uremote_query -p20141024 -h$ip -e "use cmpp_server;select response,err,fail_desc,count(*) from submit_message_send_history where yw_code = $yw_code and insert_time > DATE_ADD(now(),INTERVAL -20 MINUTE) group by 1,2,3 order by 4 desc limit 3;" | xargs` && curl --data "account=yunwei&passwd=123&emailwarning=1&email=yunwei@baiwutong.com&smswarning=1&mobile=$alarm_value&content=$server_name通道：$yw_code，失败原因：$content1" http://yj.baiwutong.com:8180/PlateWarning
	fi
	if [ "${server_name:0:4}" ==  "sgip" ];then
        content1=`mysql -uremote_query -p20141024 -h$ip -e "use sgip_server;select response,err,fail_desc,count(*) from submit_message_send_history where yw_code = $yw_code and insert_time > DATE_ADD(now(),INTERVAL -20 MINUTE) group by 1,2,3  order by 4 desc limit 3;" | xargs` && curl --data "account=yunwei&passwd=123&emailwarning=1&email=yunwei@baiwutong.com&smswarning=1&mobile=$alarm_value&content=$server_name通道：$yw_code，>失败原因：$content1" http://yj.baiwutong.com:8180/PlateWarning
        fi
	if [ "${server_name:0:4}" == "smgp" ];then
        content1=`mysql -uremote_query -p20141024 -h$ip -e "use smgp_server_new;select response,err,fail_desc,count(*) from submit_message_send_history where yw_code = $yw_code and insert_time > DATE_ADD(now(),INTERVAL -20 MINUTE) group by 1,2,3  order by 4 desc limit 3;" | xargs` && curl --data "account=yunwei&passwd=123&emailwarning=1&email=yunwei@baiwutong.com&smswarning=1&mobile=$alarm_value&content=$server_name通道：$yw_code，>失败原因：$content1" http://yj.baiwutong.com:8180/PlateWarning
        fi
fi





