#!/bin/bash
month=`date -d last-month +'%Y%m'`
month1=`date -d last-month +'%Y-%m'`
path="/hskj/tmp/bjywb/bill/$month"
mkdir -p $path
mysqldump  -uyunwei -pmobile707 super_plate local_bill_detail_info --where "every_date like '$month1%'" > $path/local_bill_detail_info.sql
mysqldump  -uyunwei -pmobile707 super_plate all_user_info local_cmpp_user local_sgip_user local_smgp_user finance_info local_gate_td_info local_sms_customer_info local_customer_service_info local_sms_td_info server_info tag_info local_cluster_user_info local_cluster_user_service_info local_cluster_td_info> $path/other_info.sql
ssh root@103.26.1.158 -p10022 mkdir -p $path
scp -P10022 -r $path/* root@103.26.1.158:$path
