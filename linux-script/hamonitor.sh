#!/bin/bash 
VIP="192.168.111.3"
SIP="124.205.226.125"

3306_probe () {
  nc -w 5 -z -n $VIP 3306
}

8801_probe () {
  nc -w 5 -z -n $VIP 8801
}

3306_status () {
   local count=0
   while true
   do
    mysql_reply=`3306_probe`
    if [ ! "$mysql_reply" ];then
      ((count++))
      sleep 5
    else
      echo "MySQL 3306 is OK."
      break
    fi

   if [ "${count:-0}" -eq "5" ];then
     echo "MySQL 3306 is unreachable"
     /usr/local/bin/sendEmail -f nagios@baiwutong.com -t liuzhi@baiwutong.com -s 124.127.184.92 -u "HA $SIP mysql 3306 is unreachable" -m "HA $SIP mysql 3306 is unreachable.Start Failover." -xu nagios@baiwutong.com -xp hskj707
     service heartbeat stop && sleep 60 && service heartbeat start
     exit 1 
   fi
  done
}

8801_status () {
   local count=0
   while true
   do
    8801_reply=`8801_probe`
    if [ ! "${8801_reply}" ];then
      ((count++))
      sleep 5
    else
      echo "Master 8801 is OK."
      break
    fi

   if [ "${count:-0}" -eq "5" ];then
     echo "Master 8801 is unreachable"
     /usr/local/bin/sendEmail -f nagios@baiwutong.com -t liuzhi@baiwutong.com -s 124.127.184.92 -u "HA $SIP Master 8801 is unreachable" -m "HA $SIP Master 8801 is unreachable.Start Failover." -xu nagios@baiwutong.com -xp hskj707
     service heartbeat stop && sleep 60 && service heartbeat start
     exit 1
   fi
  done
}

vip_status () {
  ping_reply=`ping -c 10 $VIP | grep "100% packet loss" | wc -l`
  if [ $ping_reply -eq 1 ];then
    echo "ping $VIP is down!!!"
    /usr/local/bin/sendEmail -f nagios@baiwutong.com -t liuzhi@baiwutong.com -s 124.127.184.92 -u "HA Error $SIP" -m "ping $VIP is down!!!" -xu nagios@baiwutong.com -xp hskj707
    service heartbeat stop && sleep 60 && service heartbeat start
    exit 1
  else
    echo "HA failover to the backup machine."
    /usr/local/bin/sendEmail -f nagios@baiwutong.com -t liuzhi@baiwutong.com -s 124.127.184.92 -u "HA $SIP maybe failover" -m "HA failover to the backup machine." -xu nagios@baiwutong.com -xp hskj707
    exit 1
  fi
}


###########
while true
do
#check mysqld status
  ret=`service mysqld status | grep stopped | wc -l`
  if [ ${ret:-0} -eq 1 ];then
    echo "Master MySQL is stopped."
    /usr/local/bin/sendEmail -f nagios@baiwutong.com -t liuzhi@baiwutong.com -s 124.127.184.92 -u "HA $SIP Master MySQL is stopped." -m "HA $SIP Master MySQL is stopped.Start Failover." -xu nagios@baiwutong.com -xp hskj707 
    service heartbeat stop && sleep 60 && service heartbeat start
    exit 1
  else
    echo "mysqld is running."
  fi

  ret2=`/etc/ha.d/resource.d/Sgip12Gate status | grep stopped | wc -l`
  if [ ${ret2:-0} -eq 1 ];then
    echo "Master Sgip12Gate is stopped."
    /usr/local/bin/sendEmail -f nagios@baiwutong.com -t liuzhi@baiwutong.com -s 124.127.184.92 -u "HA $SIP Master Sgip12Gate is stopped." -m "HA $SIP Master Sgip12Gate is stopped.Start Failover." -xu nagios@baiwutong.com -xp hskj707
    service heartbeat stop && sleep 60 && service heartbeat start
    exit 1
  else
    echo "Sgip12Gate is running."
  fi

  ret3=`/etc/ha.d/resource.d/Sgip12Send status | grep stopped | wc -l`
  if [ ${ret3:-0} -eq 1 ];then
    echo "Master Sgip12Send is stopped."
    /usr/local/bin/sendEmail -f nagios@baiwutong.com -t liuzhi@baiwutong.com -s 124.127.184.92 -u "HA $SIP Master Sgip12Send is stopped." -m "HA $SIP Master Sgip12Send is stopped.Start Failover." -xu nagios@baiwutong.com -xp hskj707
    service heartbeat stop && sleep 60 && service heartbeat start
    exit 1
  else
    echo "Sgip12Send is running."
  fi 
   

  ret4=`/etc/ha.d/resource.d/Sgip12DataDeal status | grep stopped | wc -l`
  if [ ${ret4:-0} -eq 1 ];then
    echo "Master Sgip12DataDeal is stopped.try to restart Sgip12DataDeal"
    /etc/ha.d/resource.d/Sgip12DataDeal start
    sleep 2
    ret5=`/etc/ha.d/resource.d/Sgip12DataDeal status | grep stopped | wc -l`
    if [ ${ret5:-0} -eq 1 ];then
      /usr/local/bin/sendEmail -f nagios@baiwutong.com -t liuzhi@baiwutong.com -s 124.127.184.92 -u "HA $SIP Master Sgip12DataDeal is stopped." -m "HA $SIP Master Sgip12DataDeal is stopped.Start Failover." -xu nagios@baiwutong.com -xp hskj707
      service heartbeat stop && sleep 60 && service heartbeat start
      exit 1
    else
      echo "Master Sgip12DataDeal is running now."
    fi
  else
    echo "Sgip12DataDeal is running."
  fi 
   
reply=`3306_probe`
if [ ! "$reply" ];then
      echo "MySQL port is down!!! Continue to detect"
      ip a | grep "192.168.111.3"
      ret6=$?
      if [ $ret6 -eq 0 ];then
        echo "$VIP is running in local."
        ret7=`service mysqld status | grep running | wc -l`
        if [ $ret7 -eq 1 ];then
          echo "MySQL is running in local."
          3306_status
        else 
          echo "MySQL is down.Failover start"
          /usr/local/bin/sendEmail -f nagios@baiwutong.com -t liuzhi@baiwutong.com -s 124.127.184.92 -u "HA Failover" -m "HA failover $SIP" -xu nagios@baiwutong.com -xp hskj707
          service heartbeat stop && sleep 60 && service heartbeat start
          exit 1
        fi
      else 
        vip_status
      fi
else 
  echo "MySQL 3306 is OK."
fi

reply2=`8801_probe`
if [ ! "$reply" ];then
  echo "8801 port is down!!! Continue to detect"
  ip a | grep "192.168.111.3"
      ret8=$?
      if [ $ret8 -eq 0 ];then
        echo "$VIP is running in local."
        netstat -ntlp | grep 8801
        ret9=$?
        if [ $ret9 -eq 0 ];then
          8801_status
        else
          service heartbeat stop && sleep 60 && service heartbeat start
          exit 1
        fi
     else
       vip_status
     fi
else
  echo "Master 8801 is OK."
fi      

sleep 10
done
