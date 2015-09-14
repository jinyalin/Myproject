#!/bin/bash
datetime=$(date +%Y%m%d)
year=$(date +%Y)
month=$(date +%m)

ip="210.14.134.79"
dbname="smpp_server"

backupname=${datetime}_${ip}.tar.gz
backupdir="/backup/mysqlbackup"

mkdir -p $backupdir/$year/$month/
mkdir -p /backup/$ip/$dbname
mkdir -p /backup/$ip/system

cd /backup/$ip/$dbname
mysqldump -uhs -pV1ja89zab $dbname gate_config td_switch_info td_info thread_controller user_balance_info user_check_type user_extend_info sign_info recharge_info cache_check user_info user_service_info user_country_phone_code_price td_country_phone_code_price check_time country_phone_province_code err_code > ${dbname}_tables.sql
mysqldump -uhs -pV1ja89zab $dbname -d >  ${dbname}_structure.sql

cp /etc/my.cnf /backup/$ip/system
cp /etc/sysconfig/iptables /backup/$ip/system
cp /etc/sysconfig/network-scripts/ifcfg* /backup/$ip/system

cd /backup
tar czf $backupdir/$year/$month/$backupname  $ip

rm -rf /backup/$ip

scp -P10001 $backupdir/$year/$month/$backupname backup@124.127.184.89:/home/backup/mysqlbackup/$ip
