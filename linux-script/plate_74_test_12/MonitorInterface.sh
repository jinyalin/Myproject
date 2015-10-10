#!/bin/bash
value=`curl --data "account=yunwei&passwd=456&mobile=13261289750&smswarning=1&phonewarning=1&telphone=13261289750&content=yj.baiwutong.com is DOWN" http://yj.baiwutong.com:8180/PlateWarning`

if [ -z "${value}" ];then
/usr/local/bin/sendEmail -f nagios@baiwutong.com -t bi@hongshutech.com -t jinyalin@hongshutech.com   -s mail.baiwutong.com -u "BI预警接口故障！" -m " [http://yj.baiwutong.com:8180/PlateWarning] is down" -xu nagios@baiwutong.com  -xp hskj707
fi
