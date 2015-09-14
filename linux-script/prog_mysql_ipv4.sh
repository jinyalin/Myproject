#!/bin/bash
pid=`ps -ef | grep java | grep -v grep | awk '{print $2}' | xargs`
for i in $pid
do
  if `ps -ef | grep $i | grep -q tomcat` ;then
    echo "$(ps --no-headers -f -p $i | awk '{print $(NF - 3) }' | awk -F"=" '{print $2}') : $(netstat -antp | grep $i | awk '$5=="127.0.0.1:3306"{print $0}' | grep ESTABLISHED | wc -l)"
  else
    echo "$(ps --no-headers -f -p $i | awk '{print $NF}') : $(netstat -antp | grep $i | awk '$5=="127.0.0.1:3306"{print $0}' | grep ESTABLISHED | wc -l)"
  fi
done

echo
echo "JavaApp & MySQL TCP Connection State:"
netstat -antp | grep java | awk '$5=="127.0.0.1:3306"{print $0}' | awk '{print $(NF -1)}' | sort | uniq -c
