#!/bin/bash
pid=`ps -ef | grep java | grep -v grep | awk '{print $2}'`
for i in $pid
do
  if `ps -ef | grep $i | grep -q tomcat` ;then
    echo "$(ps --no-headers -f -p $i | awk '{print $(NF - 3) }' | awk -F"=" '{print $2}') : $(netstat -antp | grep $i | awk -F":"  '$4=="127.0.0.1"{print $0}'  | grep "3306" | grep ESTABLISHED | wc -l)"
  else
    echo "$(ps --no-headers -f -p $i | awk '{print $NF}') : $(netstat -antp | grep $i | awk -F":"  '$4=="127.0.0.1"{print $0}'  | grep "3306" | grep ESTABLISHED | wc -l)"
  fi
done

echo
echo "Java Application & MySQL TCP Connection State:"
netstat -antp | grep java | awk -F":"  '$4=="127.0.0.1"{print $0}'  | grep "3306" | awk '{print $(NF -1)}' | sort | uniq -c
