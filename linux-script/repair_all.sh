#!/bin/bash
username="hs"
password="V1ja89zab"
database="sms_client"

tables=$(mysql -u${username} -p${password} -e "use ${database};show tables")
for i in $tables
do
  mysql -u${username} -p${password} -e "use ${database};repair table ${i};"
done
