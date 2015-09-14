#!/bin/bash 
#version 1.0.0    （编写人:张家仁）

########################可配置参数严格按照格式说明配置#########################
IP=`hostname`
datetime=`date -d last-month +%Y-%m`
mysqltime="2013-201404"


mkdir /hskj/databak/${IP}-${datetime}

mysqlbackup=/hskj/databak/${IP}-${datetime}
sqlpassword="z1f7r3yalin"


#数据库删除备份
mysql_touch=1    #(0=关闭，1=开启)

#格式为：需要备份的父目录:父目录下面需要备份的子目录的文件 ;如果有同样父目录下面有多个子目录下的文件需要备份可以自己空格在添加 
mysql_dir[1]="/var/lib/mysql/sms_server"
mysql_dir[2]="/var/lib/mysql/sms_client"

#######数据库删除备份#####################
 if [ "${mysql_touch:-0}" -eq "1" ];then
   for c in ${mysql_dir[*]}
   do

      touchdir1=${c}    
      touchdir2=`ls ${c}/*201404* |awk -F "." '{print $1}' |sort -u |xargs -i -n 1 basename {}`  ##5月之前的表名
      touchdir3=`basename  ${touchdir1}`        ##库名称
      rmtouchdir4=`ls ${c}/*20* |grep -v "20140[4-6]"|awk -F "." '{print $1}' |sort -u |xargs -i -n 1 basename {}`  ##删除4月份前表
        for d in ${touchdir2}
         do
           mkdir -p ${mysqlbackup}/${touchdir3}_${mysqltime}
           mysql -udba -p${sqlpassword} -e "use "${touchdir3}";flush tables "${d}";"
           cp -rf ${touchdir1}/${d}* ${mysqlbackup}/${touchdir3}_${mysqltime}
           mysql -udba -p${sqlpassword} -e "use "${touchdir3}";flush tables "${d}";"
        done  
        
        for r in ${rmtouchdir4}
         do
           mysql -udba -p${sqlpassword} -e "use "${touchdir3}";flush tables "${r}";"
           mv ${touchdir1}/${r}* ${mysqlbackup}/${touchdir3}_${mysqltime}
           mysql -udba -p${sqlpassword} -e "use "${touchdir3}";flush tables "${r}";"
        done  
                      
        cd ${mysqlbackup}
        tar -zcvf ${touchdir3}_${mysqltime}.tar.gz ${touchdir3}_${mysqltime}
        #rm -rf ${mysqlbackup}/${touchdir3}_${mysqltime}
    done
  fi


