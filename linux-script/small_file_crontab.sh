#!/bin/bash
IP=`hostname`
datetime=`date +%Y-%m-%d`
smsfiletime=`date --date "3 days ago" +%Y%m%d`

datebackup=/hskj/databak/${IP}-${datetime}

Y=`date +%Y`
D=`date --date "3 days ago" +%m%d`

dir=/hskj/SmsSend/SmsSendWriteFile
lsdir=`ls ${dir}`
mkdir ${datebackup}
chmod 777 ${datebackup}


#备份/hskj/SmsSend/SmsSendWriteFile下的三天前目录
for i in ${lsdir}
  do
  mv ${dir}/${i}/${Y}/${D} ${datebackup}/${i}_${D}
  cd ${datebackup}
  tar -zcvf ${i}_${D}.tar.gz ${i}_${D}
  rm -rf ${datebackup}/${i}_${D}
  done

#备份/hskj/sms_file/file_info 下前一天目录
cd /hskj/sms_file/file_info
tar -zcvf sms_file_${smsfiletime}.tar.gz ${smsfiletime}
mv sms_file_${smsfiletime}.tar.gz ${datebackup}
rm -rf /hskj/sms_file/file_info/${smsfiletime}

