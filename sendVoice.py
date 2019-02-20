# -*- coding: utf-8 -*-
import requests
import json



def send_tel(tel):
    resp = requests.post(("http://voice-api.luosimao.com/v1/verify.json"),
    auth = ("api", "key-9283abe61c47499ae22c193752ed304d"),
    data = {
               "mobile": tel,
               "code": "123456"
           },
    timeout = 3,
    verify = False
    )
    result = json.loads(resp.content)
    print result

