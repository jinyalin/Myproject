#!/bin/bash
IP="183.136.131.3"
DISK_USED=`df -h |grep -v /dev/mapper/ |grep -v "Filesystem"|grep -v "文件系统"|awk '{print $(NF-1)}'|awk -F'%' '{print $1}' | xargs`
DISK_INODE_USED=`df -i |grep -v /dev/mapper/ |grep -v "Filesystem"|grep -v "文件系统"|awk '{print $(NF-1)}'|awk -F'%' '{print $1}' | xargs`

for i in $DISK_USED
do
  if [ "$i" -ge 70 ];then
    /usr/local/bin/sendEmail -f nagios@baiwutong.com -t system@hongshutech.com -s mail.baiwutong.com -u "${IP} Disk Space Usage > 70%" -m "Disk Space Usage > 70%" -xu nagios@baiwutong.com -xp hskj707
  fi
done

for i in $DISK_INODE_USED
do
  if [ "$i" -ge 70 ];then
    /usr/local/bin/sendEmail -f nagios@baiwutong.com -t system@hongshutech.com -s mail.baiwutong.com -u "${IP} Disk Space Inode Usage > 70%" -m "Disk Space Inode Usage > 70%" -xu nagios@baiwutong.com -xp hskj707
  fi
done
