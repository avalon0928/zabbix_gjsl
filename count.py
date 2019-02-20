#!/usr/bin/env python
#coding:utf-8

import pymysql
import time
import sys

# 在zabbix数据库进行指定时间区间内报警信息统计
# 命令格式：python count.py 2019022009 2019022109

TIMESTAMP="%Y%m%d%H%M"
a = sys.argv[1]
b = sys.argv[2]
redisid = 21
telid = 20
# a = '2019013112'
# b = '2019013117'
# redisid = 8
# telid = 2

def clock(inputtime):
    time.strptime(inputtime, TIMESTAMP)  # 读入为struct_time
    outtime = time.mktime(time.strptime(inputtime, TIMESTAMP))  # 变为时间戳
    return outtime


def alert_count(actionid, starttime, endtime):
    conn=pymysql.connect(host='192.168.2.121',user='root',passwd='tanglei',db='zabbix',port=3306)
    cursor = conn.cursor()
    cursor.execute("SET NAMES utf8");
    # 从mysql中读取告警信息
    sql = "SELECT count(1) FROM alerts where actionid = '%s' and clock >= '%s' and  clock <= '%s';" % (actionid, starttime, endtime)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data[0][0]


def dd_count(starttime, endtime):
    conn=pymysql.connect(host='192.168.2.121',user='root',passwd='tanglei',db='zabbix',port=3306)
    cursor = conn.cursor()
    cursor.execute("SET NAMES utf8");
    # 从mysql中读取告警信息
    sql = "SELECT sum(msgcount) FROM msg_count where ltime >= '%s' and  ltime <= '%s';" % (starttime, endtime)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data[0][0]

print("查询时间范围：%s - %s" % (a, b))
print("报警条数：%s" % alert_count(redisid, clock(a), clock(b)))
print("电话报警条数：%s" % alert_count(telid, clock(a), clock(b)))
print("告警收敛后报警条数：%s" % dd_count(a, b))
