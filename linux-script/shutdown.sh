#!/bin/sh


ps -ef| grep 'server.MainServer'|grep -v grep|awk '{print $2}'|xargs kill -9
