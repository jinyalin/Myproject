#!/bin/bash
name=`id -un`
time=$(date +'%Y-%m-%d %H:%M:%S')
ppath="/hskj/tmp/bjywb/getdate"
log="/hskj/tmp/bjywb/xd.log"
change=0
#------------------------------------------------------------------------------------------------
read -p "请输入调取详单的sql语句,不写导出文件，不写分号：" SQL
if [ ! -n "$SQL" ];then
echo "您未输入sql语句!已退出~~"
exit;
fi
read -p "请输入导出文件名：" FileName
if [ ! -n "$FileName" ];then
echo "您未输入要导出的文件名!已退出~~"
exit;
fi
read -p "请输入客服人员邮箱：" email
if [ ! -n "$email" ];then
echo "您未输入接收邮箱！已退出~~"
exit;
fi
#-------------------------------------------------------------------------------------------------
#正文部分
#执行语句查询并导出文件，压缩文件发邮件给相应客服邮箱，然后删除压缩的文件。
sql=$SQL" into outfile '$ppath/$FileName'"
echo "wait..."
/usr/bin/mysql -uyunwei -pmobile707 -e "use sms_server;$sql;"&&cd $ppath&&/bin/tar -zcvf  $FileName.tar.gz $FileName >/dev/null&&echo "${name}--${time}---tar is ok!" >> ${log}&&/usr/local/bin/sendEmail -f nagios@baiwutong.com -t ${email}  -s mail.baiwutong.com -u "sp详单" -m "附件为您申请调取的sp详单，如有问题，请联系运维同事,谢谢~"  -a $FileName.tar.gz    -xu nagios@baiwutong.com  -xp hskj707>/dev/null&&echo "${name}--${time}--${email}--sendmail is ok!" | tee -a ${log}&&rm -rf $FileName.tar.gz $FileName&&echo "${name}--${time}---rm is ok!">> ${log}&&change=1&&if [ ${change} -lt 1 ];then /usr/bin/curl --data "account=yunwei&passwd=123&phone=13261289750&content=fushen not output" http://124.127.184.89:8180/warning;fi