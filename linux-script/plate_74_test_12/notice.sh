#!/bin/bash

value=`mysql -uyunwei -pmobile707 -e "use monitor;select count(*) as count from notice_info where status=0 and insert_time < date_add(now(), INTERVAL -5 minute) ;" | grep -v "count"`

if [ $value -gt 0 ];then
cd /hskj/monitor_v2/notice
./shutdown.sh  && sleep 2 &&  ./startup.sh
curl --data "account=yunwei&passwd=123&mobile=13261289750&smswarning=1&phonewarning=1&telphone=13261289750&content=notice_info表0状态积压" http://yj.baiwutong.com:8180/PlateWarning

fi
