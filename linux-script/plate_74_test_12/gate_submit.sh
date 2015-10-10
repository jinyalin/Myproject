#! /bin/bash

mysql -uyunwei -pmobile707 -e "use monitor;select * from notice_info where insert_time > DATE_ADD(now(),INTERVAL -5 MINUTE) and  content like '%user_id%submitResp%';" | grep -v "sn" | awk -F [" ":\)\(]+ '{print "服务器： "$2,"账号: "$5,"客户提交返回错误码：  "$7" ，请及时处理~"}' | sort | uniq >  /hskj/tmp/bjywb/logs/gate_content.log
if [ -s /hskj/tmp/bjywb/logs/gate_content.log ];then
  while read line
   do
	server=`echo $line | awk '{print $2}'`
	userid=`echo $line | awk '{print $4}'`
	err=`echo $line | awk '{print $6}'`
	date=`date +%Y-%m-%d" "%H:%M:%S`
	if [ $err == '9' ];then
		line=$line"  失败原因：计费失败，余额不足，或提交的接入号不正确。"
	fi
	if [ $err == '14' ];then
		line=$line"  失败原因：8和15编码最后一条超长失败。"
	fi
	if [ $err == '15' ];then
		line=$line"  失败原因：0编码普通短信超长。"
	fi
	if [ $err == '16' ];then
		line=$line"  失败原因：8和15编码普通短信超长。"
	fi
	if [ $err == '47' ];then
		line=$line"  失败原因：非法接收号码。号码与通道不匹配。"
	fi
	if [ $err == '30' ];then
		line=$line"  失败原因：客户提交短信超过账户设置的最大速度。"
	fi
	if [ $err == '1' ];then
		line=$line"  失败原因：超速。"
	fi

	curl --data "account=yunwei&passwd=123&server=$server&userid=$userid&emailwarning=1&screenwarning=1&content=$line时间：$date" http://yj.baiwutong.com:8180/PlateWarning
        echo "$(date +%Y-%m-%d" "%H:%M:%S) $line" >> /hskj/tmp/bjywb/logs/monitor.log
  done < /hskj/tmp/bjywb/logs/gate_content.log
fi




