#! /bin/bash

mysql -uyunwei -pmobile707 -e "use monitor;select * from notice_info where insert_time > DATE_ADD(now(),INTERVAL -5 MINUTE) and content like '%send result is%';" | grep -v "sn" | awk -F [" "\)\(]+ '{print "服务器： "$2" ,账号: "$4" 提交失败返回错误码： "$8" ，请及时处理~"}' | sort | uniq   >  /hskj/tmp/bjywb/logs/sp_content.log

if [ -s /hskj/tmp/bjywb/logs/sp_content.log ];then
  while read line
   do
	server=`echo $line | awk '{print $2}'`
	userid=`echo $line | awk '{print $4}'`
	err=`echo $line | awk '{print $6}'`
	date=`date +%Y-%m-%d" "%H:%M:%S`
	if [ $err == '100' ];then
		line=$line"   失败原因：余额不足。"
	fi
	if [ $err == '101' ];then
		line=$line"   失败原因：账号关闭。"
	fi
	if [ $err == '102' ];then
		line=$line"   失败原因：短信内容超过500字或为空或内容编码格式不正确。"
	fi
	if [ $err == '103' ];then
		line=$line"   失败原因：手机号码超过200个或合法手机号码为空或者与通道类型不匹配。"
	fi
	if [ $err == '106' ];then
		line=$line"   失败原因：账号不存在。"
	fi
	if [ $err == '107' ];then
		line=$line"   失败原因：密码错误。"
	fi
	if [ $err == '108' ];then
		line=$line"   失败原因：指定访问ip错误。"
	fi
	if [ $err == '109' ];then
		line=$line"   失败原因：业务不存在或者通道关闭。"
	fi
	if [ $err == '110' ];then
		line=$line"   失败原因：小号不合法。"
	fi
	if [ $err == '112' ];then
		line=$line"   失败原因：个性化接口send_param 拆分拼凑错误。"
	fi
	if [ $err == '114' ];then
		line=$line"   失败原因：个性化接口提交应为POST，不支持GET。"
	fi
	if [ $err == '115' ];then
		line=$line"   失败原因：个性化接口total_count 与实际短信条数无法匹配，即，实际短信条数与total_count不一致。如果返回此参数，则本次提交的所有短信作废，不入库。"
	fi
	if [ $err == '116' ];then
		line=$line"   失败原因：个性化接口手机号码超过200个或合法手机号码为空。"
	fi
	curl --data "account=yunwei&passwd=123&server=$server&userid=$userid&emailwarning=1&screenwarning=1&content=$line时间：$date" http://yj.baiwutong.com:8180/PlateWarning
	echo "$(date +%Y-%m-%d" "%H:%M:%S) $line" >> /hskj/tmp/bjywb/logs/monitor.log
   done < /hskj/tmp/bjywb/logs/sp_content.log
fi




