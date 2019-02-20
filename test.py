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

actionid='8'
#连接redis，并读取所有事件id
r = redis.StrictRedis(host='192.168.2.121', port=6379, password="intest@123")

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
# msg_file = open("msg_record", "a+")
# msg_file.write(time.strftime("%Y-%m-%d %H:%M", time.localtime()) + " "+str(len(messagelist)) + "\n")
# msg_file.close()
ddcount_insert(time.strftime("%Y%m%d%H", time.localtime()), len(messagelist))

if len(messagelist) != 0:
    for content in messagelist:
        msg(content)
        # if "华菱" in content:
        #     send_tel(15222587905)   #林复坤
        # elif "灾难" in content:
        #     send_tel(13477084628)

#发送恢复信息
messagelist=compressnormal(normal)
if len(messagelist) != 0:
    for content in  messagelist:
        msg(content)
