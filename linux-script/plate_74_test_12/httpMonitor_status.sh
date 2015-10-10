#!/bin/bash
status=`find /hskj/web/Monitor/log -name "2015-10-10.info.log" -mmin -3 |wc -l`
if [ $status -ne 1 ];then
	 curl --data "account=yunwei&passwd=123&smswarning=1&mobile=13261289750,18514025566,13718894295,15321906869&content=服务器：测试机12，http监控程序出现异常，请处理！" http://103.26.1.158:8180/PlateWarning
fi
