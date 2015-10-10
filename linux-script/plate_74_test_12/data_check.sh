#!/bin/bash
month=`date -d last-month +'%Y-%m'`
cd /hskj/tmp
mysql -uroot -p123456 -e "use data_handle;select server_id, sum(total) from local_gate_data where every_month like '$month%' group by 1;" |grep -v "server_id"|sort -rn >/hskj/tmp/local_gate_data1.txt
mysql -uroot -p123456 -e "use data_handle;select server_id,sum(total) from local_gate_detail_data where every_date like '$month%'  group by 1;" |grep -v "server_id"|sort -rn >/hskj/tmp/local_gate_data2.txt
mysql -uroot -p123456 -e "use data_handle;select server_id,sum(amount) from  local_bill_detail_info where every_date like '$month%' group by 1;" |grep -v "server_id"|sort -rn >/hskj/tmp/local_gate_data3.txt

diff local_gate_data1.txt local_gate_data2.txt >/hskj/tmp/local_gate_data_all.txt
diff local_gate_data2.txt local_gate_data3.txt >>/hskj/tmp/local_gate_data_all.txt


mysql -uroot -p123456 -e "use data_handle;select server_id,sum(total),sum(success_count),sum(fail_count),sum(unknown_count) from local_gate_data where every_month like '$month%'  group by 1;" |grep -v "server_id"|sort -rn >/hskj/tmp/local_gate_data4.txt
mysql -uroot -p123456 -e "use data_handle;select server_id,sum(total),sum(success_count),sum(fail_count),sum(unknown_count) from  local_gate_detail_data where every_date like '$month%' group by 1;" |grep -v "server_id"|sort -rn >/hskj/tmp/local_gate_data5.txt
diff local_gate_data4.txt local_gate_data5.txt >/hskj/tmp/local_gate_data_Unknown.txt

mysql -uroot -p123456 -e "use data_handle;select server_id,sum(success_count) from local_gate_data where every_month like '$month%'  group by 1;" |grep -v "server_id"|sort -rn >/hskj/tmp/local_gate_data6.txt
mysql -uroot -p123456 -e "use data_handle;select server_id,sum(amount) from  local_bill_detail_info where every_date like '$month%' and err in(0,00,000,0000) group by 1;" |grep -v "server_id"|sort -rn >/hskj/tmp/local_bill_detail_info.txt
diff local_gate_data6.txt local_bill_detail_info.txt >/hskj/tmp/local_bill_detail_info_diff.txt

local_gate_data_all_wc=`cat /hskj/tmp/local_gate_data_all.txt |wc -l`
local_gate_data_Unknown_wc=`cat /hskj/tmp/local_gate_data_Unknown.txt |wc -l`
local_bill_detail_info_diff=`cat /hskj/tmp/local_bill_detail_info_diff.txt |wc -l`


if [ $local_gate_data_all_wc -eq '0' ];then
echo "local_gate_data、local_gate_detail_data、local_bill_detail_info三张表各服务器总数相同~"
else
echo "local_gate_data、local_gate_detail_data、local_bill_detail_info三张表各服务器总数存在不同，请排查!"
fi
if [ $local_gate_data_Unknown_wc -eq '0' ];then
echo "local_gate_data、local_gate_detail_data两张表各服务器成功失败未知状态都相同~"
else
echo "local_gate_data、local_gate_detail_data两张表各服务器成功失败未知状态存在不同，请排查!"
fi
if [ $local_bill_detail_info_diff -eq '0' ];then
echo "local_gate_data、local_bill_detail_info两张表各服务器成功状态都相同~"
else
echo "local_gate_data、local_bill_detail_info两张表各服务器成功存在不同，请排查!"
fi