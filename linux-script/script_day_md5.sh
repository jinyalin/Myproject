#!/bin/bash
source ~/.bash_profile
user=root
datetime=`date -d "32 day ago" +'%Y-%m-%d'`
dir="*-${datetime}"

ipaddr="218.207.183.78 210.14.134.91 210.14.134.80 210.14.134.90 211.136.105.73 211.103.155.220 210.14.134.75 218.207.183.122 183.56.167.43 218.207.183.118 210.14.134.85 103.26.1.136 210.14.134.79 58.22.109.15 58.22.109.22 124.95.129.69 210.14.134.78 183.136.131.3 211.100.6.103 211.100.6.104 211.100.34.60 211.100.34.61 210.14.134.92 111.13.132.36 115.85.192.72 210.14.156.175 61.147.118.16 103.26.1.134 111.13.132.38"

#ipaddr="172.16.10.74 210.14.156.175 118.144.76.45 218.241.153.202 211.103.155.246 211.103.155.244 118.144.76.60 118.144.76.79 211.103.155.220 211.100.34.60 211.100.34.61 211.100.6.103 211.100.6.104 210.14.134.78 210.14.134.75 218.207.183.78 58.22.109.15 58.22.109.22 111.13.132.34 183.136.131.3 115.85.192.72 211.136.105.72 211.136.105.73 124.95.129.69 61.147.118.16 210.14.134.80 210.14.134.79 172.16.10.78 172.16.10.71 210.14.134.90 210.14.134.91 210.14.134.92 218.207.183.118 218.207.183.122 183.56.167.43"

for md5 in ${ipaddr}
  do
    cd /hskj/databackup/${md5}/${dir}
    md5sum *tar.gz >md5_bak.txt
    echo "/hskj/databackup/${md5}/${dir}" >>/hskj/databackup/md5/${datetime}_md5.txt
    diff md5.txt md5_bak.txt >>/hskj/databackup/md5/${datetime}_md5.txt 2>&1
    ls -trl /hskj/databackup/${md5}/${dir} >>/hskj/databackup/md5/${datetime}_md5.txt
    echo "############################################################" >>/hskj/databackup/md5/${datetime}_md5.txt
  done
   echo "##############################详细信息############################" >>/hskj/databackup/md5/${datetime}_md5.txt
   cd /hskj/databackup/
   ll */*2014-10 >>/hskj/databackup/md5/${datetime}_md5.txt  

  /usr/local/bin/sendEmail -f nagios@baiwutong.com -t zhangjiaren@baiwutong.com -s mail.baiwutong.com -u "每天备份上传" -m "`cat /hskj/databackup/md5/${datetime}_md5.txt`" -xu nagios@baiwutong.com -xp hskj707 



