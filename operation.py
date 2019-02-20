#!/usr/bin/python
# coding:utf-8
import datetime,time


# 告警合并 originallist为告警信息list
def mergeproblem(originallist):
    problemlist=[]
    normalist=[]
    Unknown=[]
    triggerkeylist=[]
    sorts=[]
    alarminfo=[]
    #告警or恢复
    for origina in originallist:
        # 汇总告警list
        if origina['triggervalue']=='1' :
            problemlist.append(origina)
            # 汇总故障类型list
            if origina['triggerkey'] not in triggerkeylist:
                triggerkeylist.append(origina['triggerkey'])
        else:
            Unknown.append(origina)

    for triggerkey in triggerkeylist:
        for problem in problemlist:
            # 根据triggerkey将故障信息list中元素分类汇总
            if problem['triggerkey']==triggerkey:
                sorts.append(problem)
        # alarminfo为分类汇总后的故障信息集合
        alarminfo.append(sorts)
        sorts=[]
    return alarminfo


# 恢复合并
def mergenormal(originallist):
    normallist=[]
    Unknown=[]
    triggerkeylist=[]
    sorts=[]
    alarminfo=[]
    #告警or恢复
    for origina in originallist:
        # 汇总告警list
        if origina['triggervalue']=='0' :
            normallist.append(origina)
            # 汇总故障类型list
            if origina['triggerkey'] not in triggerkeylist:
                triggerkeylist.append(origina['triggerkey'])
        else:
            Unknown.append(origina)

    for triggerkey in triggerkeylist:
        for normal in normallist:
            if normal['triggerkey']==triggerkey:
                sorts.append(normal)
        alarminfo.append(sorts)
        sorts=[]
    return alarminfo

#告警压缩
def compressproblem(alarminfo):
    # 记录分析时间
    currenttime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    messagelist=[]
    # 分类报警
    for info in alarminfo:
        hostlist=''
        # 每一类报警中有多少条告警信息
        infonum=len(info)
        # 告警输出
        for host in info:
            triggername=host['triggername']
            hostinfo=host['triggernseverity']+':'+host['hostname']+'\n'
            hostlist+=hostinfo
        # 同类报警 数量在3-6间
        if infonum >= 1 and infonum <= 6:
            message='告警主机:'+str(infonum)+'台\n'+hostlist+'告警项目:'+triggername+'\n'+'分析时间:'+currenttime
            messagelist.append(message)
        # 同类报警 数量超过6
        elif infonum > 6:
            message='大量告警主机:'+str(infonum)+'台\n'+'告警项目:'+triggername+'\n'+'分析时间:'+currenttime
            messagelist.append(message)
    return messagelist


#恢复压缩
def compressnormal(alarminfo):
    currenttime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    messagelist=[]
    for info in alarminfo:
        hostlist=''
        infonum=len(info)
        for host in info:
            triggername=host['triggername']
            hostinfo=host['triggernseverity']+':'+host['hostname']+'\n'
            hostlist+=hostinfo
        if infonum >= 1 and infonum <= 6:
            message='恢复主机:'+str(infonum)+'台\n'+hostlist+'告警项目:'+triggername+'\n'+'分析时间:'+currenttime
            messagelist.append(message)
        elif infonum > 6:
            message='大量恢复主机:'+str(infonum)+'台\n'+'告警项目:'+triggername+'\n'+'分析时间:'+currenttime
            messagelist.append(message)
    return messagelist