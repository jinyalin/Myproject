#!/bin/bash

118.16HA1(){
     echo -e "\033[33m ���ݵ��ŷ����� HA1 118.16 \033[0m"
     echo -e "test hskj"
}

118.16HA2(){
     echo -e "\033[33m ���ݵ��ŷ����� HA2 118.16 \033[0m"
     echo -e "test hskj"
}

echo -e "###############ѡ�������############\033[0m"
echo -e "1:       ���ݵ��ŷ����� HA1     \033[0m"
echo -e "2:       ���ݵ��ŷ����� HA2    \033[0m"

echo -e "\033[31m ��ѡ��: \033[0m";read RESPONSE


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