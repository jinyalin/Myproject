#! /bin/bash

mysql -uyunwei -pmobile707 -e "use monitor;select * from notice_info where insert_time > DATE_ADD(now(),INTERVAL -1 MINUTE) and content like '%通道名称%';" | grep -v "sn" |awk -F [:" "\)\(]+ '{print $2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14":"$15}'|sort | uniq > /hskj/tmp/bjywb/logs/file_info_submit_content.log


if [ -s /hskj/tmp/bjywb/logs/file_info_submit_content.log ];then
  cat /hskj/tmp/bjywb/logs/file_info_submit_content.log >> /hskj/tmp/bjywb/logs/file_info_submit.log
  while read line
   do
	td_code=`echo $line | awk '{print $6}'`
	td_name=`echo $line | awk '{print $3}'`
	server=`echo $line | awk '{print $1}'`
	var=`echo $td_name | grep "独享"`
	if [ "$var" != "" ];then
		userid=`mysql -uyunwei -pmobile707 -e "use super_plate;select user_id from local_user_service_info where td_code=$td_code and server_id='$server' and status=0"| grep -v "user_id" | sort | uniq`
		message1=`curl --data "account=yunwei&passwd=123&server=$server&userid=$userid&emailwarning=1&smswarning=1&screenwarning=1&content=$line" http://yj.baiwutong.com:8180/PlateWarning`
                message11=`curl --data "account=yunwei&passwd=123&screenwarning=1&screenuser=1012079,1008031,1306352,1405412,1104108&smswarning=1&mobile=13269317987,13269317987,15201549663,15210020155,15501209980&content=$line" http://yj.baiwutong.com:8180/PlateWarning`
                echo $message1 >> /hskj/tmp/bjywb/logs/file_info_submit.log
                echo $message11 >> /hskj/tmp/bjywb/logs/file_info_submit.log
	else
		message2=`curl --data "account=yunwei&passwd=123&emailwarning=1&email=hskj@hongshutech.com,bwkf@hongshutech.com,xskf@hongshutech.com,yykf@hongshutech.com&smswarning=1&mobile=13261289750,13269317987,15210446863,15801596667,15810971125,18501303565,18911342625,15201549663,15210020155,15501209980&content=$line" http://yj.baiwutong.com:8180/PlateWarning`
               echo $message2 >> /hskj/tmp/bjywb/logs/file_info_submit.log
	fi
   done < /hskj/tmp/bjywb/logs/file_info_submit_content.log
fi




