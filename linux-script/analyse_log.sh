#!/bin/bash
date=`date +'%Y%m%d-%H%M%S'`

###Configure Area
ip="192.168.5.36"
analyse_log_dir="/root/analyse/analyse_log"

mkdir -p ${analyse_log_dir}

log[1]="/root/analyse/log/info1.log"
analyse_log_name1="info1"
command1() {
  awk '/send result/{print $5,$6,$7,$8,$9}' ${log[i]} | sort -k1 | uniq -c
}

log[2]="/root/analyse/log/info2.log"
analyse_log_name2="info2"
command2() {
  awk '/send result/{print $5,$6,$7,$8,$9}' ${log[i]} | sort -k1 | uniq -c
}

log[3]="/root/analyse/log/info3.log"
analyse_log_name3="info3"
command3() {
  awk '/send result/{print $1}' ${log[i]} | sort -k1 | uniq -c
}

###
for((i=1;i<=3;i++))
do
  analyse_log_name=$(eval echo "\$analyse_log_name${i}")
  analyse_log_name_path=${analyse_log_dir}/${analyse_log_name}_${date}.log
  echo ${analyse_log_name_path} 
  command$i > ${analyse_log_name_path}
  count=$(wc -l ${analyse_log_name_path} | awk '{print $1}')
  if [ "${count:0}" -ne 0 ];then
    /usr/local/bin/sendEmail -f nagios@baiwutong.com -t lz@baiwutong.com -s mail.baiwutong.com -u "$ip analyse ${log[i]}" -m "`cat ${analyse_log_name_path}` " -xu nagios@baiwutong.com -xp hskj707
  fi
done





