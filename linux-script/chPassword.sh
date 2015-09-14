#!/bin/bash
user=`id -un`
email="jinyalin@hongshutech.com"
echo "以下为查询可重启线上程序的账号信息："
read -p "请输入工号：" number
if [ ! -n $number ];then
echo "工号未输入，已退出~"
exit 0
fi
if [ $number != "1012079" -a $number != "1210284" -a $number != "1107139" -a $number != "1112196" -a $number != "1204230" ];then
echo "非法工号，已退出~"
exit 0
fi
if [ $number == "1012079" ];then
email="jinyalin@hongshutech.com"
fi
if [ $number == "1210284" ];then
email="pcp@hongshutech.com -t jinyalin@hongshutech.com"
fi
if [ $number == "1107139" ];then
email="yzm@hongshutech.com -t jinyalin@hongshutech.com"
fi
if [ $number == "1112196" ];then
email="zxt@hongshutech.com -t jinyalin@hongshutech.com"
fi
if [ $number == "1204230" ];then
email="zjy@hongshutech.com -t jinyalin@hongshutech.com"
fi
a=(a b c d e A B C D E F @ $ % ^ 0 1 2 3 4 5 6 7 8 9)
password=`for ((i=0;i<10;i++));do echo -n ${a[$RANDOM % ${#a[@]}]};done`
expect -c "set timeout -1;
spawn su - root
expect -re "密码：" {send \"yunwei1208\r\";exp_continue}  -re "]$" {send \"echo yunwei:$password |chpasswd && su - $user \r\"};
interact"
/usr/local/bin/sendEmail -f nagios@baiwutong.com -t ${email}  -s mail.baiwutong.com -u "（重要）密码查询结果" -m "服务器：192.168.5.5\n 操作系统登录账号：yunwei\n操作系统登录密码：$password \n 此密码具有一定时效性，请尽快处理问题~"   -xu nagios@baiwutong.com  -xp hskj707 




