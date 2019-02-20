#!/usr/bin/python
# coding:utf-8

import pymysql
import time


# 定义通过actionid和subject获取数据库告警具体信息，并以字典形式返回
def alerts_eventid(actionid,subject):
        try:
                # 连接zabbix mysql库
                conn=pymysql.connect(host='192.168.2.121',user='root',passwd='tanglei',db='zabbix',port=3306)
                cursor = conn.cursor()
                cursor.execute("SET NAMES utf8");
                # subject = alerts.subject = actions.def_shortdata，即从redis中读取的eventid
                # 从mysql中读取告警信息
                sql = "SELECT * FROM alerts where actionid = '%s' and subject = '%s' ;" % (actionid, subject)
                cursor.execute(sql)
                data = cursor.fetchall()
                cursor.close()
                conn.close()
                event = data[0]
                messagelist = []
                message = event[8]
                # 根据#号切割告警信息
                messageone = message.split('#')
                # 将切割后的消息，通过分隔符|改为键值结构
                for i in messageone:
                        messagelist.append(i.split('|'))
                messagedict = dict(messagelist)
                return messagedict
        except pymysql.Error,e:
                print("Mysql Error %d: %s" % (e.args[0], e.args[1]))


def ddcount_insert(ltime, msgcount):
    try:
        # 连接zabbix mysql库
        conn = pymysql.connect(host='192.168.2.121', user='root', passwd='tanglei', db='zabbix', port=3306)
        cursor = conn.cursor()
        cursor.execute("SET NAMES utf8");
        # subject = alerts.subject = actions.def_shortdata，即从redis中读取的eventid
        # 从mysql中读取告警信息
        sql = "INSERT INTO msg_count1 (ltime, msgcount) VALUES ( %s, %d ) ;" % (ltime, msgcount)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    except pymysql.Error, e:
        print("Mysql Error %s: %d" % (ltime, msgcount))
#
# ltime = time.strftime("%Y%m%d%H%M", time.localtime())
# ddcount_insert(ltime, 10)


