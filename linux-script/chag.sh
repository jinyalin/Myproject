#!/bin/bash
time=$(date +'%Y-%m-%d %H:%M:%S')
user=`id -un`
echo "******查询可重启线上程序的账号信息******"
read -p "请输入工号：" number
    if [ ! -n $number ];then
       echo "工号未输入，已退出~"
       exit 0
    fi
    if [ $number != "1012079" -a $number != "1210284" -a $number != "1107139" -a $number != "1112196" -a $number != "1204230" ];then
       echo "非法工号，已退出~"
       exit 0
    fi
a=(a b c d e A B C D E F @ $ % ^ 0 1 2 3 4 5 6 7 8 9)
password=`for ((i=0;i<10;i++));do echo -n ${a[$RANDOM % ${#a[@]}]};done`
echo "用户：$user , 调用了查询yunwei密码,时间：$time" >>/hskj/tmp/bjywb/chpasswd.log
/usr/local/bin/sendEmail -f nagios@baiwutong.com -t jinyalin@hongshutech.com  -s mail.baiwutong.com -u "密码查询调用通知！" -m "用户：$user ，调用了查询yunwei密码，新>密码为：$password 时间：$time "   -xu nagios@baiwutong.com  -xp hskj707
expect -c "set timeout -1;
spawn su - root
expect -re "密码：" {send \"yunwei1208\r\";exp_continue}  -re "]#" {send \"echo wuqiang:$password |chpasswd && su - $user \r\";exp_continue} -re "]$" {send \"echo 服务器：192.168.5.5  登录账号：yunwei  登录密码：$password \r\"};
interact"


