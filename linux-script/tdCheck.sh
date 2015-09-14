#!/bin/bash

#切换响应码说明：
#  0   请求成功
#-11 业务代码填写为空
#-13 用户状态关闭
#-14 业务代码不存在或者没有备用通道可切换
#-15 备用通道不存在
#-16 账户没有使用该业务或者账户业务不支持切换

time=$(date +'%Y-%m-%d %H:%M:%S')
cd /hskj/send/log

SokectInfo=`tail -200 info.log | egrep -a "socket to ip.*failure" | awk -F [" ":]+ '{print $9}' | sort | uniq -c | awk '$1>2{print $2}' |xargs`
#SGIP_01 SMGP_01
LoginInfo=`tail -200 info.log | grep -a "loginResp:" | grep -v "loginResp:0" | awk -F [:" "]+ '{print $(NF-5)}' | sort |uniq -c | awk '$1>2{print $2}'|xargs`
#SMGP_01
SubmitInfo=`tail -200 info.log | grep -a "submitResp:" | grep -v "submitResp:0" | awk -F [" ":]+ '{print $(NF-5)}' | sort | uniq -c  | awk '$1>2{print $2}'|xargs`
#SMGP_01

for td in ${SokectInfo}
do
    if [  -n $td ];then
    value=`curl --data "td_code=${td}" http://192.168.6.223:8080/gateway_client/cClientTdChange.do`
    echo "${time} SokectError tdChange ${td} result is ${value}" >> /hskj/script/BusinessMonitor/TdCodeCheck/tdChange.log
    fi
done

for td in ${LoginInfo}
do
    if [  -n $td ];then
    value=`curl --data "td_code=${td}" http://192.168.6.223:8080/gateway_client/cClientTdChange.do`
    echo "${time} LoginError tdChange ${td} result is ${value}" >> /hskj/script/BusinessMonitor/TdCodeCheck/tdChange.log
    fi
done

for td in ${SubmitInfo}
do
    if [  -n $td ];then
    value=`curl --data "td_code=${td}" http://192.168.6.223:8080/gateway_client/cClientTdChange.do`
    echo "${time} SubmitError tdChange ${td} result is ${value}" >> /hskj/script/BusinessMonitor/TdCodeCheck/tdChange.log
    fi
done




