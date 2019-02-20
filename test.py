#!/usr/bin/env python
#coding:utf-8
import pymysql
import redis
import sys
from dbread import *
from operation import *
from dingding import *
import datetime,time
from sendVoice import *

sendtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

actionid='21'
#连接redis，并读取所有事件id
r = redis.StrictRedis(host='172.16.5.102', port=6379, password="intest@123")

# 本地测试信息
# actionid='8'
# #连接redis，并读取所有事件id
# r = redis.StrictRedis(host='192.168.2.121', port=6379, password="intest@123")

# 将redis中消息取出赋值后，清空redis
subjectlist=r.keys()
for i in subjectlist:
    r.delete(i)
# r.flushdb()
# 根据redis中的subject从mysql取值，存入list
originallist=[]
for subject in subjectlist:
    a=alerts_eventid(str(actionid), subject)
    originallist.append(a)

problem = mergeproblem(originallist)
normal = mergenormal(originallist)


#发送告警信息
messagelist=compressproblem(problem)
ddcount_insert(time.strftime("%Y%m%d%H", time.localtime()), len(messagelist))
if len(messagelist) != 0:
    for content in messagelist:
        msg(content)
        if "北汽" in content:
            send_tel(17521573073)   #丁亚运
            send_tel(18071091691)

#发送恢复信息
messagelist=compressnormal(normal)
if len(messagelist) != 0:
    for content in  messagelist:
        msg(content)