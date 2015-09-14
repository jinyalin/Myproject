#!/bin/bash
IP="183.136.131.3"
PD_Num=8

source /etc/profile

Critical_PD=$(MegaCli -AdpAllInfo -aALL | grep "Critical Disks" | awk '{print $NF}')
Failed_PD=$(MegaCli -AdpAllInfo -aALL | grep "Failed Disks" | awk '{print $NF}')
Online_PD=$(MegaCli -PdList -aALL | grep 'Firmware state' | grep -c Online)
Degraded_VD=$(MegaCli -AdpAllInfo -aALL | grep "Degraded" | awk '{print $NF}')
Offline_VD=$(MegaCli -AdpAllInfo -aALL | grep "  Offline" | awk '{print $NF}')

MegaCli -AdpAllInfo -aALL | grep -A9 "Device Present"
MegaCli -PdList -aALL  |egrep 'Firmware state|Slot Number'

echo

if [ "${Critical_PD}" -ne "0" -o "${Failed_PD}" -ne "0" -o "${Degraded_VD}" -ne "0" -o "${Offline_VD}" -ne "0" -o "${Online_PD}" -ne "${PD_Num}" ];then
  echo ":-) Status: Critical!"
  /usr/local/bin/sendEmail -f nagios@baiwutong.com -t system@hongshutech.com -s mail.baiwutong.com -u "$IP Disk Error" -m "Disk Error: Please run MegaCli -AdpAllInfo -aALL | grep -A9 'Device Present'" -xu nagios@baiwutong.com -xp hskj707 
else
  echo ":-) Status: Normal."
fi
