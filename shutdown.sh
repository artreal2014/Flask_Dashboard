#!/bin/bash 

ps -ef | grep '/home/sysop/HR_LarkDashboard/wsgi.py'

ppid=`ps -ef | grep /home/sysop/HR_LarkDashboard/wsgi.py | grep -v grep| awk '{print $3}'`
if [[ "$ppid" == "1" ||  "$ppid" == "" ]]
then
    echo "No parent process to kill"
else
    kill -9 $ppid
    echo "Killed $ppid"
fi

pid=`ps -ef | grep /home/sysop/HR_LarkDashboard/wsgi.py | grep -v grep| awk '{print $2}'`
if [["$pid" != "" ]]
then 
    kill -9 $pid
    echo "Killed $pid"
else
    echo "No child process to kill"
fi 
