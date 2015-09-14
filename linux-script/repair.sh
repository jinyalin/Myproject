#!/bin/bash
username="hs"
password="V1ja89zab"
database="sms_client"

tables=$(mysql -u${username} -p${password} -e "use ${database};show tables" | sed -n '2,$p' | grep -v "[0-9]$" | xargs)
for i in $tables
do
  mysql -u${username} -p${password} -e "use ${database};repair table ${i};"
done
