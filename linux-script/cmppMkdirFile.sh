#!/bin/sh

cd /usr/local/cmppSend/
mkdir smgpSendWriteFile
mkdir smgpSend_Log
cd smgpSendWriteFile
rm -fr ./
mkdir file_info_deliver
mkdir file_info_deliverDisposed
mkdir file_info_map
mkdir file_info_mapDisposed
mkdir file_info_report
mkdir file_info_reportDisposed
mkdir file_info_send
mkdir file_info_sendDisposed
mkdir smgpSms
mkdir smgpSmsDisposed


cd /usr/local/cmppSend/smgpSend_Log/
rm -fr ./
mkdir api 
mkdir CheckedMsgToFileThread
mkdir controlOtherMethod
mkdir DAO
mkdir dealEveryDayCount
mkdir report
mkdir send
mkdir sendThread
mkdir smgp_scanThread
mkdir timeDealThread

cd /usr/local/
mkdir cmppbi
cd cmppbi
rm -fr ./


