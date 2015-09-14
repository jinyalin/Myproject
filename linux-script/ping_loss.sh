#!/bin/bash
# 填写要ping ip 多ip 空格隔开

ip="183.232.39.41"

# 写明要停止的时间 年月日时分
time="201610151031"


date=`date +%Y%m%d%H%M`
while [ "${date}" -le "${time}" ]
 do
   for i in ${ip}
    do
    echo `date` >ping_${i}.txt
    ping -i 0.5 -c 10 ${i} >>ping_${i}.txt
    loss=`grep "packet" ping_${i}.txt |awk -F "%" '{print $1}' |awk '{print $NF}'`
    losscount=1
    while [ "${loss}" -gt 5 ]
       do
         if [ ${losscount} -eq 3 ] || [ ${losscount} -eq 9 ] || [ ${losscount} -eq 360 ];then
         /usr/local/bin/sendEmail -f nagios@baiwutong.com -t system@hongshutech.com yunwei@baiwutong.com -s mail.baiwutong.com -u "ping ${i} loss ${loss}% err" -m "ping ${i} loss ${loss}% err" -xu nagios@baiwutong.com  -xp hskj707
         curl --data "account=system&passwd=123&content=ping ${i} loss ${loss}%&telphone=15201186062,18511891207&phonewarning=1" http://yj.baiwutong.com:8180/PlateWarning
         curl --data "account=system&passwd=123&content=ping ${i} loss ${loss}%&mobile=15201186062,18511891207&smswarning=1" http://yj.baiwutong.com:8180/PlateWarning
         fi
        sleep 10
        mv ping_${i}.txt /hskj/backup/ping/ping_${i}_${date}.txt
        echo `date` >ping_${i}.txt
        ping -i 0.5 -c 10 ${i} >>ping_${i}.txt
        loss=`grep "packet" ping_${i}.txt |awk -F "%" '{print $1}' |awk '{print $NF}'`
        losscount=`/usr/bin/expr ${losscount} + 1`    
         if [ ${loss} -lt 5 ] &&  [ ${losscount} -gt 3 ] ;then
         /usr/local/bin/sendEmail -f nagios@baiwutong.com -t system@hongshutech.com yunwei@baiwutong.com  -s mail.baiwutong.com -u "ping ${i} loss ${loss}% restore" -m "ping ${i} loss ${loss}% restore" -xu nagios@baiwutong.com  -xp hskj707
         curl --data "account=system&passwd=123&content=ping ${i} recover ${loss}%&telphone=15201186062,18511891207&phonewarning=1" http://yj.baiwutong.com:8180/PlateWarning
         curl --data "account=system&passwd=123&content=ping ${i} recover ${loss}%&mobile=15201186062,18511891207&smswarning=1" http://yj.baiwutong.com:8180/PlateWarning
         fi   
      done 
    done
  sleep 10
 done