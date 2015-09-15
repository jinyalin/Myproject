#!/bin/bash
# 填写要ping ip 多ip 空格隔开

while :
do
 local_ip=`mysql -uyunwei -pmobile707 -e "use temp;select ip from local_ip;" |grep -v "ip" |xargs`
 allow_ip=`mysql -uyunwei -pmobile707 -e "use temp;select ip from allow_ip;" |grep -v ${local_ip} |grep -v "ip" |xargs`


 datedir=`date +%Y%m%d%H%M%S`

 mkdir /hskj/script/pinglog
 mkdir /hskj/logs/ping
 rm -rf /hskj/script/pinglog/*

 for i in ${allow_ip}
   do
    ping -i 0.5 -c 10 ${i} >/hskj/script/pinglog/${i} &
   done
 
 sleep 22
 psping=`ps -ef |grep "ping -i 0.5 -c 10" |grep -v "grep" |wc -l`

# 结果输出成bi使用格式
  if [ ${psping} -eq 0 ];then
    cat /hskj/script/pinglog/* >>/hskj/logs/ping/${local_ip}_${datedir}
  else
   sleep 2
   psping=`ps -ef |grep "ping -i 0.5 -c 10" |grep -v "grep" |wc -l`
   if [ ${psping} -ne 0 ];then
    /usr/local/bin/sendEmail -f nagios@baiwutong.com -t system@hongshutech.com -s mail.baiwutong.com -u "${local_ip} ping err" -m "`ps -ef |grep "ping -i 0.5 -c 10" |grep -v "grep"`" -xu nagios@baiwutong.com -xp hskj707 
    kill -9 `ps -ef |grep "ping -i 0.5 -c 10" |grep -v "grep"|awk '{print $2}'`
   fi
  fi
sleep 5
done
