#!/bin/bash
datetime=`date +%Y%m%d`
dir=`ls -tl /rz/${datetime}/${LOGNAME}/|grep "-"|head -1|awk '{printf $NF}'`
cat /rz/${datetime}/${LOGNAME}/${dir}|grep -v "#"
