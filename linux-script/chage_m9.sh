#!/bin/bash
value=`grep -a "M9" a.txt | wc -l`
if [[ $value -eq 0 ]];then
sed -i 'a\\n#on/off   M9模块控制开关\nmonitor.status.M9=on\n#最近3分钟以内的状态报告匹配数据（成功率监控）\nmonitor.model.009=M9\nmonitor.class.M9=com.hskj.form.SmsMessage\nmonitor.filter.M9=matched_message\nmonitor.condition.M9=new Date().getTime() - (new Date((msg_sendTime.substr(0,20)).replace(/-/g,'/'))).getTime() < 180000 ;\nmonitor.variable.M9=yw_code:yw_code,response:response,msg_sendTime:msg_sendTime\nmonitor.frequency.M9=60000\nmonitor.name.M9=match2\nmonitor.key.M9=var v_key_value; if(response==0){ v_key_value='\\''+yw_code+'\\',0';}else {v_key_value='\\''+yw_code+'\\',2';}'  a.txt
fi
