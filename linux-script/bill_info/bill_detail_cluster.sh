#! /bin/bash
path="/hskj/tmp/bjywb/bill_detail.log"
month=$(date -d '4 days ago' +%Y%m)
day=$(date -d '4 days ago' +%Y-%m-%d)
#day='2015-08-31'
sname="cluster_server"
uname="user_info"
table=`mysql -uyunwei -pmobile707 -e "use $sname;show tables like \"submit_message_send_history_$month\";" | grep -v "Tables_in"`
table1=`mysql -uyunwei -pmobile707 -e "use temp;show tables like \"detail_$month\";" | grep -v "Tables_in"`
if [ $table1 ];then
        detail_table="insert into temp.detail_"$month" select date(insert_time) as date,user_id,td_code,sp_number,err,price,sum(charge_count) as amount from "$sname".submit_message_send_history_"$month" where insert_time like  '$day%' group  by 1,2,3,4,5,6;"
else
        detail_table="create table temp.detail_"$month" select date(insert_time) as date,user_id,td_code,sp_number,err,price,sum(charge_count) as amount from "$sname".submit_message_send_history_"$month" where insert_time like '$day%' group  by 1,2,3,4,5,6;"
fi

if [ $table ];then
        echo "$day日数据开始执行------------------------>" >> $path
        echo "$day日数据统计开始执行时间：$(date +'%Y-%m-%d %H:%M:%S')"  >> $path && mysql -uyunwei -pmobile707 -e "$detail_table" && echo "$day日数据统计执行完成时间：$(date +'%Y-%m-%d %H:%M:%S')"  >> $path && echo "$day日账单数据开始生成时间：$(date +'%Y-%m-%d %H:%M:%S')" >> $path && mysql -uyunwei -pmobile707 -e "insert into "$sname".bill_detail_info(every_date,user_id,user_name,user_sp_number,td_code,td_name,td_sp_number,err,price,amount) select d.date,d.user_id,u.user_name,d.sp_number,d.td_code,t.td_name,t.td_sp_number,d.err,d.price,sum(d.amount)  from temp.detail_"$month"  d,(select td_name,td_code,td_sp_number from "$sname".td_info group by 1,2,3) t,"$sname"."$uname" u where d.td_code=t.td_code and u.user_id=d.user_id and d.date like '$day%' group by d.td_code,d.user_id,d.err,d.date,d.price;" && echo "$day日账单数据生成完毕时间：$(date +'%Y-%m-%d %H:%M:%S')"  >> $path
        echo "$day日数据执行结束-----------------------!!!"  >> $path
else
        echo "$(date +'%Y-%m-%d %H:%M:%S')-要统计的月份表submit_message_send_history_$month不存在~" >> $path
fi
