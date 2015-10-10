#!/bin/bash
#td_failure_rate
mysql -udba -psmshskj1207 -e "use monitor;update server_monitor_info set value=90 where monitor_sn =10 or monitor_sn=141;"
mysql -udba -psmshskj1207 -e "use monitor;update monitor_info set alarm_type='phone,sms' where sn =10 or monitor_sn=141;"
#file_info*
mysql -udba -psmshskj1207 -e "use monitor;update monitor_info set alarm_type='phone,sms' where sn in (1,2);"
