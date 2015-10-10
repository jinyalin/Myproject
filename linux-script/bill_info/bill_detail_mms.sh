#! /bin/bash
path="/hskj/tmp/bjywb/bill_detail.log"
month=$(date -d '4 days ago' +%Y%m)
day=$(date -d '4 days ago' +%Y-%m-%d)
sname="mms"
month_table=`mysql -uyunwei -pmobile707 -e "use $sname;show tables like \"mms_submit_cdma_$month\";" | grep -v "Tables_in"`
if [ $month_table ];then
        echo "$day日账单开始执行------------------------>" >> $path
        echo "$day日账单数据开始生成时间：$(date +'%Y-%m-%d %H:%M:%S')" >> $path 
        tables="mms_submit_cdma_$month mms_submit_un_$month mms_submit_cm_$month mms_submit_cm_history mms_submit_cdma_history mms_submit_un_history mms_submit_cm mms_submit_cdma mms_submit_un"
        for table in $tables
           do
	 	mysql -uyunwei -pmobile707 -e "insert into $sname.bill_detail_info (every_date,user_id,user_name,user_sp_number,td_code,td_name,td_sp_number,err,price,amount)(select date(s.insert_time),u.user_id,u.user_name,CONCAT(t.td_sp_number,s.ext_code) ,t.td_code,t.td_name,t.td_sp_number,s.result,s.price,count(*) from $sname.$table s,$sname.td_info t,$sname.user_info u where s.mmstd=t.td_code and u.user_sn=s.user_sn and s.insert_time like '$day%' group by s.mmstd,s.user_sn,s.result,date(s.insert_time));" 
	   done
 	echo "$day日账单数据生成完毕时间：$(date +'%Y-%m-%d %H:%M:%S')"  >> $path
        echo "$day日账单执行结束-----------------------!!!"  >> $path
else
        echo "$(date +'%Y-%m-%d %H:%M:%S')-要统计的月份表mms_submit_cdma_$month不存在~" >> $path
fi
