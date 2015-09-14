#!/bin/bash
#written by liuzhi 2013/05/27 version 2

nohup[1]="/hskj/SmsSend/nohup.out"
nohup[2]="/hskj/Cmpp20Gate/nohup.out"
nohup[3]="/hskj/self_gate_dealdata_2_0_39_11/nohup.out"
nohup[4]="/hskj/SystemMonitor/nohup.out"

for i in ${nohup[*]}
do
  cat /dev/null > $i
done
