#!/bin/bash

value=`find /hskj/tmp/bjywb -mtime -1 -name "chpasswd.log" |wc -l`

if [ $value -gt 0 ];then
a=(a b c d e A B C D E F @ $ % ^ 0 1 2 3 4 5 6 7 8 9)
password=`for ((i=0;i<10;i++));do echo -n ${a[$RANDOM % ${#a[@]}]};done`
echo yunwei:$password |chpasswd
/usr/local/bin/sendEmail -f nagios@baiwutong.com -t jinyalin@hongshutech.com  -s mail.baiwutong.com -u "密码更新通知" -m "新密码为：$password 时间：$time "   -xu nagios@baiwutong.com  -xp hskj707
fi
