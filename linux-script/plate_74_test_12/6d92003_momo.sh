#! /bin/bash

content=`mysql -uyunwei -pmobile707 -e "use monitor;select content count from  notice_info where content like '%陌陌%' and insert_time > DATE_ADD(now(),INTERVAL -5 MINUTE) limit 1;" | grep -v "content"`
if [ "$content" != "" ];then

failure_rate=`echo "$content" | awk '{print $3}'`
success_rate=`echo "$content" | awk '{print $5}'`

	if [[ ${failure_rate} -ge 10 ]] && [[ ${success_rate} -lt 85 ]];then
		content1=`mysql -uremote_query -p20141024 -h172.16.10.90 -e "use cmpp_server;select response,err,fail_desc,count(*) from submit_message_send_history where (user_sn=792 or user_sn=1630) and insert_time > DATE_ADD(now(),INTERVAL -10 MINUTE) group by 1,2,3 order by 4 desc limit 3;" | xargs`
		sleep 2
		curl --data "account=yunwei&passwd=123&emailwarning=1&email=jinyalin@hongshutech.com,malimin@baiwutong.com&smswarning=1&mobile=13261289750,15201186062&content=陌陌预警原因展示（cmpp75账号:hs3001,user_sn=792）：$content1" http://yj.baiwutong.com:8180/PlateWarning
	fi
fi





