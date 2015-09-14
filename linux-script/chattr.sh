#!/bin/bash
datetime=`date +%Y%m%d`
lsdir=`ls /rz/${datetime}`

for i in ${lsdir}
   do
     chattr +a /rz/${datetime}/${i}/*
   done
