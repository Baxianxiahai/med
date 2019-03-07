'''
Created on 2018年12月28日

@author: Administrator
'''

# import random
# import sys
# import time
# import json
# import os
# import re
# import urllib
# import http
# import socket
# import datetime
# import string
# import ctypes 
# import random
# import cv2 as cv
# import numpy as np
# import matplotlib.pyplot as plt
# import math
# from   ctypes import c_uint8
# import urllib
import urllib3
# import requests
# import socket
# import pycurl
# import io
# import certifi  #导入根证书集合，用于验证SSL证书可信和TLS主机身份
# from io import BytesIO
# from urllib.parse import urlencode
import json
# import http.client


class TupClsHuijsonItf(object):
    '''
    classdocs
    '''

    def __init__(self, svrAddr, svrPort):
        '''
        Constructor
        '''
        _TUP_HUIJSON_SVR_ADDR = svrAddr
        _TUP_HUIJSON_SVR_PORT = svrPort
    
    #建立长连接的链路
    #可能需要考虑建立一个实时接收任务进行监控
    def socket_setup(self):
        pass

    def socket_disc(self):
        pass

    def socket_data_snd(self):
        pass

    def socket_data_rcv(self):
        pass
    
    #无连接，一次性发送
    def curl_data_snd(self, jsonInputData):
        encoded_data = json.dumps(jsonInputData).encode('utf-8')
        http = urllib3.PoolManager(maxsize=10, timeout=30.0, block=True)
        r = http.request(
            'POST',
            self._TUP_HUIJSON_SVR_ADDR,
            body=encoded_data, 
            headers={'Content-Type':'application/json', 'Connection': 'close'}
            )
        try:
            result = json.loads(r.data)
        except Exception:
            print("HUIJSON: Not fetch right feedback!")
            result = ''
        return result




















    
    