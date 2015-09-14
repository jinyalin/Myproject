#!/bin/bash
export ORACLE_BASE=/u01/app/oracle
export ORACLE_HOME=$ORACLE_BASE/product/10.2.0/db_1
export ORACLE_SID=hskj
export PATH=$PATH:$ORACLE_HOME/bin
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/lib:/usr/lib
export CLASSPATH=$ORACLE_HOME/JRE:$ORACLE_HOME/jlib:$ORACLE_HOME/rdbms/jlib

su - oracle -c "export ORACLE_SID=hskj"
su - oracle -c "source /u01/oracle/.bash_profile"
su - oracle -c "dbstart"
su - oracle -c "lsnrctl start"
su - oracle -c "emctl start dbconsole"
su - oracle -c "isqlplusctl start"