#!/bin/bash
#written by lz 2015/1/14

service="acpid auditd bluetooth cups yum-updatesd nfslock avahi-daemon NetworkManager postfix iptables ip6tables"
datetime=$(date '+%Y%m%d%H%M')
cur_dir=$(pwd)

if grep -q "CentOS release 6" /etc/issue ;then
  echo ":-) Current system version is `head -1 /etc/issue`."
else
  echo "ERROR Current system is not *CentOS 6* Series Linux."
  exit 1
fi

if [ `uname -m` == "x86_64" ];then
  echo ":-) Current system is an x86_64 version."
else
  echo "ERROR Current system is NOT an *x86_64* version."
  exit
fi

#check if root is runing the script
if [ $(id -u) != "0" ];then
  echo "ERROR You must be *ROOT* to run this script."
  exit 1
else
  echo '====== :-) Here we go. ======'
fi

create_user () {
  if grep -q 'hstest' /etc/passwd ;then
    echo 'ERROR hstest user already exist, now exit shell script.'
    exit 1
  else
    echo "Now add system account: hstest"
    useradd -d /hskj -m hstest; echo 'hongshu.com2015' | passwd --stdin hstest

    cp -rf /etc/skel/.bash* /hskj/
    chmod 755 /hskj/
    chown hstest.hstest /hskj/
    chown hstest.hstest /hskj/.bash*

    mkdir -p /hskj/tmp && chmod 777 /hskj/tmp
    mkdir -p /hskj/databak && chmod 777 /hskj/databak
    mkdir -p /hskj/script && chmod 777 /hskj/script
    mkdir -p /hskj/backup  && chmod 777 /hskj/backup
  fi  
}

init_system () {
  rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-6
  yum -y install vim* wget gcc gcc-c++ automake autoconf vixie-cron ntp sysstat iotop system-config-firewall-tui system-config-lvm system-config-network-tui lsof tcpdump telnet traceroute flex byacc libpcap ncurses ncurses-devel libpcap-devel
  yum -y groupinstall "Development Tools"
  chmod u+s /usr/sbin/lsof
  chmod u+s /usr/sbin/tcpdump
  cd $cur_dir
  rpm -ivh packages/nload-0.7.4-1.el6.rf.x86_64.rpm
  rpm -ivh packages/iftop-1.0-0.7.pre4.el6.x86_64.rpm
  cp $cur_dir/packages/sendEmail /usr/local/bin/sendEmail
  chmod a+x /usr/local/bin/sendEmail
  mkdir -p /hskj/script
  cp $cur_dir/script/* /hskj/script
  
  yum -y groupinstall "Chinese Support"
  sed -i '/LANG/s/.*/LANG="zh_CN.UTF-8"/g' /etc/sysconfig/i18n
  export LANG="zh_CN.UTF-8"

  for i in $service
  do
    chkconfig $i off
    service $i stop
  done

  service crond start
  chkconfig crond on
  echo '20 1 * * * /usr/sbin/ntpdate ntp.api.bz;/sbin/hwclock -w > /dev/null 2>&1' >> /tmp/crontab2.tmp
  crontab /tmp/crontab2.tmp
  rm -f /tmp/crontab2.tmp
 
cat << EOF >> /etc/sysctl.conf
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv4.ip_local_port_range = 1024 65000
EOF
  
  sed -i '/SELINUX/s/enforcing/disabled/' /etc/selinux/config

  echo "* soft nofile 65535" >> /etc/security/limits.conf
  echo "* hard nofile 65535" >> /etc/security/limits.conf
  echo "session   required        /lib64/security/pam_limits.so" >> /etc/pam.d/login
  sed -i 's/1024/65535/g' /etc/security/limits.d/90-nproc.conf
  sysctl -p
}


install_jdk () {
  cd $cur_dir
  rpm -ivh packages/jdk-6u26-linux-amd64.rpm
  
cat << EOF >> /etc/profile
JAVA_HOME=/usr/java/jdk1.6.0_26
PATH=\$JAVA_HOME/bin:\$PATH:.
CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export JAVA_HOME
export PATH
export CLASSPATH
EOF
  
  source /etc/profile
}

check_jdk () {
   v=$(java -version 2>&1)
   pos=$(expr match "$v" 'java version \"1.6.0_26\"')
   if [ $pos -gt 0 ];then
     echo "java version "1.6.0_26" has installed."
     exit 1
   else
     echo "Now install jdk: java version "1.6.0_26"."
     install_jdk
   fi     
}

install_mysql () {
  yum -y install mysql mysql-server
  cd $cur_dir
  yes | cp -f conf/my.cnf  /etc/my.cnf
  setenforce 0
  service mysqld restart
  /usr/bin/mysqladmin -u root password 'hongshu.com2015'

cat > /tmp/mysql_sec_script<<EOF
use mysql;
update user set password=password('hongshu.com2015') where user='root';
delete from user where not (user='root') ;
delete from user where user='root' and password=''; 
DROP USER ''@'%';
grant all privileges on *.* to 'root'@'%' identified by 'hongshu.com2015';
flush privileges;
EOF

mysql -u root -phongshu.com2015 -h localhost < /tmp/mysql_sec_script
rm -f /tmp/mysql_sec_script
chkconfig mysqld on
}

install_tomcat () {
  mkdir -p /hskj
  cd $cur_dir
  tar -xzvf packages/apache-tomcat-6.0.43.tar.gz -C /hskj/
  cd /hskj
  mv apache-tomcat-6.0.43 tomcat
  chown -R hstest.hstest /hskj/tomcat  
} 

read -p "Option:
         (system)
         (user)
         (jdk)
         (tomcat)
         (mysql)
         (all)
         :-) I choose:" choice
case $choice in
system)
    init_system
    ;;
user)
    create_user
    ;;
jdk)
    check_jdk
    ;;
tomcat)
    install_tomcat
    ;;
mysql)
    install_mysql
    ;;
all)
    init_system
    create_user
    check_jdk    
    install_tomcat
    install_mysql
    ;;
*)
    echo "Please input (system | user | jdk | tomcat | mysql | all)."
    exit 1
esac
