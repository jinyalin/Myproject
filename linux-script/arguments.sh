#!/bin/sh
echo "script name:$0"
echo "first argument:$1"
echo "second argument:$2"
echo "argement number:$#"
echo "arguments:$@"
echo "show param list:$*"
echo "show process id:$$"
nohup ping www.baidu.com &
echo "last background process pid: $!"
echo "show precess exit stat: $?"
