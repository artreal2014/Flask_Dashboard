#!/bin/bash

CWD="$HOME/HR_LarkDashboard"
LOG="$HOME/HR_LarkDashboard/log/log.log"

bash shutdown.sh

echo "Starting the dashboard server ..."
nohup python3 $CWD/wsgi.py >>$LOG 2>&1 &
sleep 10
ps -ef | grep '/home/sysop/HR_LarkDashboard/wsgi.py'
echo "Done..."