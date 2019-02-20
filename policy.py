#!/usr/bin/env python
# coding:utf-8
import redis
import sys

try:
    subject = sys.argv[1]
    # subject = '123'
    r = redis.StrictRedis(host='192.168.2.121', port=6379)
    r.set(subject, subject)
except Exception as e:
    print(Exception)

