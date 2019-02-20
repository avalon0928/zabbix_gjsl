# vi /usr/lib/zabbix/alertscripts/zabbix_dingding.py
#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import sys
import os



def msg(text):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    api_url = "https://oapi.dingtalk.com/robot/send?access_token=f1235c352e3f2aae15c3e72ad8fd4f3a8eec0a956149cfb6862393842acd3db2"
    json_text= {"msgtype": "text","text": {"content": text},"at": {"atMobiles": ["13477084628"],"isAtAll": True}}
    print requests.post(api_url,json.dumps(json_text),headers=headers).content

# if __name__ == '__main__':
#     text = sys.argv[1]
# msg("123")
