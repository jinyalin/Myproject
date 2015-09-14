#!/bin/bash

118.16HA1(){
     echo -e "\033[33m 扬州电信服务器 HA1 118.16 \033[0m"
     echo -e "test hskj"
}

118.16HA2(){
     echo -e "\033[33m 扬州电信服务器 HA2 118.16 \033[0m"
     echo -e "test hskj"
}

echo -e "###############选择服务器############\033[0m"
echo -e "1:       扬州电信服务器 HA1     \033[0m"
echo -e "2:       扬州电信服务器 HA2    \033[0m"

echo -e "\033[31m 请选择: \033[0m";read RESPONSE


case $RESPONSE in

1)
        118.16HA2
        exit 0
        ;;

2)
        118.16HA2
        exit 0
        ;;
                                                                
esac

exit $RETVAL