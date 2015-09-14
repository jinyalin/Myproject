#!/bin/bash
user=root
source ~/.bash_profile
datetime=`date -d "3 day ago" +'%Y%m'`
dir="*${datetime}*"
ipaddr="123.125.243.46"

for ip in ${ipaddr}
  do
   {
    mkdir /hskj/databackup/${ipaddr}
    rsync -vzrtp -P  root@${ip}:/hskj/databak/wushang/${dir} /hskj/databackup/${ip}
    rsync -vzrtp -P  root@${ip}:/hskj/databak/wushang/md5.txt /hskj/databackup/${ip}
    }
  done


find /hskj/databackup/${ipaddr} -name "*.tar.gz" -mtime +40 | xargs rm -rf

cd /hskj/databackup/${ipaddr}
md5sum *${dir}.tar.gz >md5_bak.txt
diff md5.txt md5_bak.txt >${datetime}_md5.txt 2>&1
du -sh /hskj/databackup/${ip}/*${dir}.tar.gz >>${datetime}_md5.txt
 /usr/local/bin/sendEmail -f nagios@baiwutong.com -t zhangjiaren@baiwutong.com -s mail.baiwutong.com -u "悟商每天备份上传" -m "`cat /hskj/databackup/${ipaddr}/${datetime}_md5.txt`" -xu nagios@baiwutong.com -xp hskj707
