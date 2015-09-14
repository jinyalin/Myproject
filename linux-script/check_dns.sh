#/bin/bash
system_ip="172.16.210.2"
backup_ip="218.207.183.122"
current_ip=`dig mysql.baiwutong.com +short`

pid=$(ps -ef | grep "tomcat_check" | grep -v grep | awk '{print $2}')

check_start() {
  if [ -n "$pid" ];then
    echo "Process status is normal."
  else
    cd /hskj/tomcat_check/bin && ./startup.sh
    echo "Startup process."
  fi
}

check_stop() {
  if [ -n "$pid" ];then
    cd /hskj/tomcat_check/bin && ./shutdown.sh
    echo "Shutdown process."
  else
    echo "Process status is normal."
  fi
}

check_ping() {
  count=0
  ip_list="210.14.134.254 210.14.134.253 210.14.134.252"
  for i in $ip_list
  do
    loss=`ping -c 2 $i | grep "loss" | awk -F "%" '{print $1}' |awk '{print $NF}'`
    count=`expr $count + $loss`
  done
}

if [ "$current_ip" = "$system_ip" ];then
  check_start
elif [ "$current_ip" = "$backup_ip" ];then
  check_stop
else
  check_ping
  if [ $count -eq 300 ];then
    check_stop    
  fi
fi

