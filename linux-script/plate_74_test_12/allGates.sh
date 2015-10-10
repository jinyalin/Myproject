#!/bin/bash

change=`find /hskj/monitor_v2/allGates/logs  -mmin -2 -name "system_monitor.log" |wc -l`

if [ $change -lt 1 ];then

    value=`curl --data "account=yunwei&passwd=123&mobile=13261289750&smswarning=1&phonewarning=1&telphone=13261289750&content=74 /hskj/monitor_v2/allGates/logs/system_monitor.log is down" http://yj.baiwutong.com:8180/PlateWarning`

fi
