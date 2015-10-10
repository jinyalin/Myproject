#! /bin/bash
path="/hskj/tmp/bjywb/bill_check.log"
month=$(date -d '4 days ago' +%Y%m)
day=$(date -d '4 days ago' +%Y-%m-%d)
sname="cmpp_server"
table=`mysql -uyunwei -pmobile707 -e "use $sname;show tables like \"submit_message_send_history_$month\";" | grep -v "Tables_in"`
if [ $table ];then

echo "$day日核对开始执行------------------------>" >> $path
echo "查询开始时间：$(date +'%Y-%m-%d %H:%M:%S')" >> $path
bill_count=`mysql -uyunwei -pmobile707 -e "select sum(amount) from $sname.bill_detail_info where every_date like '$day%'"| grep -v "sum"`
history_count=`mysql -uyunwei -pmobile707 -e "select sum(charge_count) from $sname.submit_message_send_history_$month where insert_time like '$day%'"| grep -v "sum"`
statistic_count=`mysql -uyunwei -pmobile707 -e "select sum(amount) from $sname.submit_history_statistic where date like '$day%'"| grep -v "sum"`
echo "查询完毕时间：$(date +'%Y-%m-%d %H:%M:%S')" >> $path
echo "对比开始时间：$(date +'%Y-%m-%d %H:%M:%S')" >> $path
if [ $bill_count -gt $history_count ];then
	value=$(($bill_count-$history_count))
	if [ $value -lt 10 ];then
		echo "$day日--账单表数量$bill_count和下发月份表总数量$history_count差额在10条以内，近似相同~" >> $path
	else
		echo "$day日--ERROR:账单表数量$bill_count-下发月份表总数量$history_count=${value}条,请排查！！！" >> $path
	fi
fi

if [ $bill_count -lt $history_count ];then
        value=$(($history_count-$bill_count))
        if [ $value -lt 10 ];then
                echo "$day日--账单表数量$bill_count和下发月份表总数量$history_count差额在10条以内，近似相同~" >> $path
        else
                echo "$day日--ERROR:下发月份表总数量$history_count-账单表数量$bill_count=${value}条,请排查！！！" >> $path
	fi
fi


if [ $bill_count == $history_count ];then
	echo "$day日--账单表数量$bill_count和下发月份表总数量$history_count完全相同~" >> $path
fi


if [ $bill_count -gt $statistic_count ];then
        value=$(($bill_count-$statistic_count))
        if [ $value -lt 500 ];then
                echo "$day日--账单表数量$bill_count和统计表总数量$statistic_count差额在500条以内，近似相同~" >> $path
        else
                echo "$day日--ERROR:账单表数量$bill_count-统计表总数量$statistic_count=${value}条,请排查！！！" >> $path
	fi
fi

if [ $bill_count -lt $statistic_count ];then
        value=$(($statistic_count-$bill_count))
        if [ $value -lt 500 ];then
                echo "$day日--账单表数量$bill_count和统计表总数量$statistic_count差额在500条以内，近似相同~" >> $path
        else
                echo "$day日--ERROR:统计表总数量$statistic_count-账单表数量$bill_count=${value}条,请排查！！！" >> $path
	fi
fi


if [ $bill_count == $statistic_count ];then
        echo "$day日--账单表数量$bill_count和统计表总数量$statistic_count完全相同~" >> $path
fi

echo "对比结束时间：$(date +'%Y-%m-%d %H:%M:%S')" >> $path
echo "$day日核对执行结束------------------------!!!" >> $path

else
echo "$(date +'%Y-%m-%d %H:%M:%S')-要核对的月份表submit_message_send_history_$month不存在~" >> $path
fi

