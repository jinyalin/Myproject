#!/bin/bash

mysql -udba -psmshskj1207 -e "use monitor;update server_monitor_info set value=300 where monitor_sn in (8,15,22);"
