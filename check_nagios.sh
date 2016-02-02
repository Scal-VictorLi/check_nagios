#!/bin/bash

TEL=18098814335
MIP=172.18.8.135
MDIR=/root/check_nagios
MONITORLOG=log/monitor_$(/bin/date +"%Y-%m-%d").log
HISTORYLOG=log/monitor_$(/bin/date -d last-week +"%Y-%m-%d").log
ALARM="监控系统二期服务器WEB页面无法访问，请立即处理。"
RECOVERY="监控系统二期服务器WEB页面恢复正常。"
status_notification=`/bin/awk '{print $3}' /root/check_nagios/status_notification`

/bin/ping -c 5 $MIP > /dev/null 2>&1
if [ "$?" = "0" ] ; then
	$MDIR/check_http -I $MIP -p 80 -u /index.php -e 200 > /dev/null 2>&1
	if [ "$?" = "0" ]; then
		if [ "$status_notification" = "1"  ];then
			/bin/echo "status_notification = 0" > $MDIR/status_notification
			/bin/date +'%Y-%m-%d %X' >> $MDIR/$MONITORLOG
			/usr/local/python3.4/bin/python3.4 $MDIR/sendsms.py $TEL $RECOVERY >> $MDIR/$MONITORLOG 2>&1
			#/bin/echo "the monitor server is alive now!" >> $MDIR/$MONITORLOG
		else
			/bin/date +'%Y-%m-%d %X' >> $MDIR/$MONITORLOG
                        /bin/echo "the status of notification is lasting!" >> $MDIR/$MONITORLOG
		fi
	else
		if [ "$status_notification" = "0"  ];then
                	/bin/echo "status_notification = 1" > $MDIR/status_notification
                	/bin/date +'%Y-%m-%d %X' >> $MDIR/$MONITORLOG
			/usr/local/python3.4/bin/python3.4 $MDIR/sendsms.py $TEL $ALARM  >> $MDIR/$MONITORLOG 2>&1
		else
			/bin/date +'%Y-%m-%d %X' >> $MDIR/$MONITORLOG
			/bin/echo "the status of notification is lasting!" >> $MDIR/$MONITORLOG
		fi
	fi
else
	if [ "$status_notification" = "0"  ];then
		/bin/echo "status_notification = 1" > $MDIR/status_notification
        	/bin/date +'%Y-%m-%d %X' >> $MDIR/$MONITORLOG
		/usr/local/python3.4/bin/python3.4 $MDIR/sendsms.py $TEL $ALARM  >> $MDIR/$MONITORLOG 2>&1
	else
		/bin/date +'%Y-%m-%d %X' >> $MDIR/$MONITORLOG
		/bin/echo "the status of notification is lasting!" >> $MDIR/$MONITORLOG
	fi		
fi

/bin/rm -rf $MDIR/$HISTORYLOG
