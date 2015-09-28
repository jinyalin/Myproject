#!/bin/bash

name="五八同城ws0778信息统计"

datetime=`date  +%Y-%m-%d`

database="cmpp_server"

#发送总量：
send_count=`grep -a "receiver - send submitResp" /hskj/logs/gate/receiver.txt | grep -ac "user_id : ws0778"`
 
#连接数
for ip in 219.141.179.84 211.151.115.31 211.151.115.28 211.151.115.4 211.151.115.229 106.2.163.162
 do
   count=`netstat -an  | grep -ac $ip`
   count1=$(($count1+$count))
 done


# 峰值
spike=`grep -a "receiver - send submitResp" /hskj/logs/gate/receiver.txt| grep -a "user_id : ws0778" | awk -F "," '{print $1}' | sort | uniq -c | sort -k1 -nr | head -1`

#重连情况：
reconnect=`grep -a "login" /hskj/logs/gate/receiver.txt | grep -a "ws0778" |wc -l`

#状态报告交互环节
sqlcount=`mysql -uhs -pV1ja89zab -e "use "${database}";select count(*) as count from report_message where user_sn=1702 and status=0 and timestampdiff(second, insert_time, now()) > 120;"|grep -v "count"`
 
  if [ ${sqlcount} -eq "0" ];then
    ms="状态报告交互环节正常"
  else
    ms="状态报告交互环节异常"
  fi

echo ${datetime} 截止目前 >/hskj/script/yw.txt
echo 1:发送总量：${send_count} >>/hskj/script/yw.txt
echo 2.连接数：${count1} >>/hskj/script/yw.txt
echo 3.峰值速度：${spike} >>/hskj/script/yw.txt
echo 4.重连次数：${reconnect} >>/hskj/script/yw.txt
echo 5.${ms} >>/hskj/script/yw.txt

/usr/local/bin/sendEmail -f nagios@baiwutong.com -t songyunfeng@58.com wangpeng02@58.com  xuyuxin@baiwutong.com zl@hongshutech.com 1491432364@qq.com  -s mail.baiwutong.com -u "${name}" -m "`cat /hskj/script/yw.txt`" -xu nagios@baiwutong.com -xp hskj707
