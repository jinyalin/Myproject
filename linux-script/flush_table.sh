#!/bin/bash
username="root"
password="lztest2014"
database="db1"

tables=$(mysql -u${username} -p${password} -e "use ${database};show tables" | sed -n '2,$p' | xargs)
for i in $tables
do
  mysql -u${username} -p${password} -e "use ${database};flush table ${i};"
done

