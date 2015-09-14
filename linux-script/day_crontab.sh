#!/bin/bash 
#version 1.0.0    （编写人:张家仁）

########################可配置参数严格按照格式说明配置#########################
IP=`hostname`
datetime=`date --date "30 days ago" +%Y-%m-%d`
datetime2=`date -d "60 days ago" +%Y-%m-%d`

shell_log=/hskj/databak/day_crontab.log
freesum=/hskj/databak/freedisk_month


#数据日志文件删除备份
date_touch=1  #(0=关闭，1=开启)

#格式为：需要备份的父目录路径:父目录下面需要备份的子目录目录/备份文件(多个文件直接冒号分开添加即可)
cptouch_dir[1]="/hskj/smpp_deal_data|/Log/*"${datetime}""
cptouch_dir[2]="/hskj/smppGate|/log/*"${datetime}""
cptouch_dir[3]="/hskj/SmsSend|/log/*"${datetime}""

#备份父目录名称
tartouch="smpp_deal_data smppGate SmsSend"



############################脚本部分 尽量不修改########################

#创建备份目录
mkdir /hskj/databak/${IP}-${datetime}
chmod 777 /hskj/databak/${IP}-${datetime}
datebackup=/hskj/databak/${IP}-${datetime}


#######数据日志文件备份删除30天前数据 删除60天前备份文件 生成md5校验文件#####################
 if [ "${date_touch:-0}" -eq "1" ];then
   for e in ${cptouch_dir[*]}
   do
      echo "cptouch_dir ${e} `date` start" >>${shell_log} 
      dir01=`echo ${e}|awk -F "|" '{print $1}'`
      dir02=`echo ${e}|awk -F "|" '{print $2}'`
      cptouch1=`dirname  ${dir02}`    
      cptouch2=`basename ${dir02} |sed 's/:/ /g'`
      cptouch3=`basename  ${dir01}`    
        for f in ${cptouch2}
         do
           mkdir -p ${datebackup}/${cptouch3}_${datetime}${cptouch1}
           mv ${dir01}${cptouch1}/${f}* ${datebackup}/${cptouch3}_${datetime}${cptouch1}
        done        
        echo "cptouch_dir ${e}  `date` END" >>${shell_log}
        echo "-----" >>${shell_log}
    done
    for f in ${tartouch}
     do
      cd ${datebackup}
      tar -zcvf ${f}_${datetime}.tar.gz ${f}_${datetime}
      rm -rf ${f}_${datetime}
      cd
     done
  fi

cd /hskj/databak/${IP}-${datetime}
md5sum *tar.gz > /hskj/databak/${IP}-${datetime}/md5.txt
rm -rf /hskj/databak/${IP}-${datetime2}

