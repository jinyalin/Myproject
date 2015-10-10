#!/bin/bash
month=`date -d last-month +'%Y%m'`
path="/hskj/tmp/bjywb/bill/$month"
FileNames=`ls $path/*`
for file in $FileNames
    do
        mysql -uroot -p123456 -e "use data_handle;source $file;"
    done

