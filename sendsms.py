#!/usr/local/python3.4/bin/python3.4
import urllib.request
import os
import json
import sys,time
#ISOTIMEFORMAT = '%Y-%m-%d %X'
os.chdir("/root/check_nagios/log")

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def senddata():
    send_url = 'http://172.18.8.169:18080/api/message/send'
    telnum = '18098814335' 
    datetime = time.strftime("%Y-%m-%d %X",time.localtime( time.time())) 
    date = time.strftime("%Y-%m-%d",time.localtime( time.time())) 
    content = '监控服务器于' + datetime + '出现服务无法响应,请立即检查!'
    log = open("monitor_"+date+".log","a")
    print(content,file=log)
    postDict = {
        'tel'      : telnum,
        'msg'      : content
	               }	
    postData = urllib.parse.urlencode(postDict).encode(encoding='UTF8')
    send_request = urllib.request.Request(send_url,postData)
    response = urllib.request.urlopen(send_request)
#返回平台信息，调试时比较有用
    msg = response.read()
    print(msg)
senddata()
