#!/bin/sh
#version 1.0.0    （编写人:张家仁）

########################可配置参数严格按照格式说明配置#########################
IP=`hostname`
dirtime=`date +%Y%m%d`
shell_log=/hskj/script/weekly_cront.log
datetime=`date +%Y-%m`
backup=/hskj/databak/${IP}-${datetime}
mkdir /hskj/databak/${IP}-${datetime}
chmod 777 /hskj/databak/${IP}-${datetime}

#剪切备份文件夹，并重新创建新文件夹
mv_mkdir=1   #(0=关闭，1=开启)
#需要剪切备份目录（最后不能加/）
mvmkdir_dir[1]="/hskj/Sgip12Send/sgipSendWriteFile"

freesum=/hskj/databak/weekly_month



############################脚本部分 尽量不修改#################


freedisk_now=`df | grep '/$' | awk '{print $(NF-2)}'`
freedisk_last=`cat ${freesum}`
increase=`expr ${freedisk_last} - ${freedisk_now}`

if [ ${increase} -ge ${freedisk_now} ];then
  echo "`date` free disk shortage!" >>${shell_log}
  /usr/local/bin/sendEmail -f nagios@baiwutong.com -t liuzhi@baiwutong.com zhangjiaren@baiwutong.com -s mail.baiwutong.com -u "${IP} backup freedisk shortage" -m "${IP} backup freedisk shortage" -xu nagios@baiwutong.com -xp hskj707
exit 1
else

#############剪切备份文件夹，并重新创建新文件夹###############
if [ "${mv_mkdir:-0}" -eq "1" ];then
   for a in ${mvmkdir_dir[*]}
   do
      echo "mv_mkdir  ${a} `date` start" >>${shell_log}
      dirname=`basename $a`
      funame=`dirname ${a} |xargs basename`
      mkdir -p ${backup}/${dirname}_${funame}_${dirtime}

      lsdir=`ls ${a}`
      mv ${a} ${a}_bak
      mkdir ${a}
        for b in ${lsdir}
         do
          mkdir ${a}/${b}
         done
      mv ${a}_bak ${backup}/${dirname}_${funame}_${dirtime}
      cd ${backup}
      echo "-----" >>${shell_log}
      echo "tar ${dirname}_${funame}_${dirtime} `date` start"  >>${shell_log}
      tar -zcvf ${dirname}_${funame}_${dirtime}.tar.gz ${dirname}_${funame}_${dirtime}
      echo "tar ${dirname}_${funame}_${dirtime} `date` edd"  >>${shell_log}
      echo "-----" >>${shell_log}
      rm -rf ${dirname}_${funame}_${dirtime}
      cd
    echo "mv_mkdir ${a} `date` edd" >>${shell_log}
    echo "-----" >>${shell_log}
    done
 fi

fi
