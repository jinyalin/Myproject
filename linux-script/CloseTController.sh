#!/bin/bash

sn=`mysql -uroot -p123456 -e "use sms_server;select sn from thread_controller where status=3;" | grep -v "sn" | xargs`

if [ -n "$sn" ];then
   for i in $sn
     do
       mysql -uroot -p123456 -e "use sms_server;update thread_controller set status=4 where sn =$i;"
     done
   /hskj/sendlib/sp_send_thread/shutdown.sh
   /hskj/sendlib/sp_send_thread/startup.sh
fi
