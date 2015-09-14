#!/bin/sh

program="com.hskj.thread.MainSever"
deploypath="/hskj/Deliver32Send"

pid=$(ps -ef| grep "$program" | grep -v grep|awk '{print $2}')
datetime=$(date +'%Y %m %d %H:%M:%S')

cd $deploypath

if [ -n "$pid" ];then
  echo "$program is already running"
else
  if [ -f nohup.out ];then
    rm -f nohup.out
  fi
  touch nohup.out && chmod  o+r nohup.out

  nohup java -Xms1024m -Xmx2048m -Djava.ext.dirs=lib -cp . $program &>nohup.out &
  echo "$datetime $program start" >> restart.log
fi
