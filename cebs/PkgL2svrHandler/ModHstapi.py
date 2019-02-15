'''
Created on 2018年12月28日

@author: Administrator
'''

import random
import sys
import time
import json
import os
import re
import urllib
import http
import socket
import datetime
import string
import ctypes 
import random
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import math
from   ctypes import c_uint8
import urllib
import urllib3
import requests
import socket
import pycurl
import io
import certifi  #导入根证书集合，用于验证SSL证书可信和TLS主机身份
from io import BytesIO
from urllib.parse import urlencode
import json
import http.client

class TupClsHstapiBasic(object):
    '''
    classdocs
    '''
    _TUP_HST_URL_SVR_ADDR = 'http://localhost:7999/post'

    def __init__(self):
        '''
        Constructor
        '''
    
    #测试好使的
    #jsonInputData  = {"restTag":"dba","actionId":3800,"parFlag":1,"parContent":{"cmd":"add","user":"test222"}}
    def hstCurlPost(self, jsonInputData):
        encoded_data = json.dumps(jsonInputData).encode('utf-8')
        http = urllib3.PoolManager(maxsize=10, timeout=30.0, block=True)
        r = http.request(
            'POST',
            self._TUP_HST_URL_SVR_ADDR,
            body=encoded_data, 
            headers={'Content-Type':'application/json', 'Connection': 'close'}
            )
        try:
            result = json.loads(r.data)
        except Exception:
            print("HSTAPI: Not fetch right feedback!")
            result = ''
        return result

    #编码过程
    def hstapiEncode(self, restTag, actionId, parFlag, parContent):
        outputJson = {}
        outputJson['restTag'] = restTag
        outputJson['actionId'] = actionId
        if (parFlag == 1) or (parFlag == True) or len(parContent)>1:
            outputJson['parFlag'] = len(parContent)
        else:
            outputJson['parFlag'] = 0
        if (outputJson['parFlag'] == 0):
            outputJson['parContent'] = {}
        else:
            outputJson['parContent'] = parContent
        return outputJson
    
    #解码过程
    def hstapiDecode(self, inputJson):
        print("inputJson",inputJson)
        restTag = 'NONE'
        actionId = -1
        parFlag = -1
        parContent = {}
        if ('restTag' in inputJson):
            restTag = inputJson['restTag']
        if ('actionId' in inputJson):
            actionId = inputJson['actionId']
        if ('parFlag' in inputJson):
            parFlag = inputJson['parFlag']
        if ('parContent' in inputJson):
            parContent = inputJson['parContent']
        return restTag, actionId, parFlag, parContent

    #试图使用pycurl方案，没成功    
    def hstPycurlPost(self):
        buffer = BytesIO()  #创建缓存对象
        hstUrl = 'http://localhost:7999/'
        post_data = {"restTag":"dba","actionId":3800,"parFlag":1,"parContent":{"cmd":"add","user":"test222"}}
        c = pycurl.Curl()
        #c.setopt(pycurl.VERBOSE, 1) #提示是否带完整的头部
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.MAXREDIRS, 5)
        c.setopt(pycurl.AUTOREFERER, 1)
        c.setopt(pycurl.CONNECTTIMEOUT, 60)
        c.setopt(pycurl.TIMEOUT, 300)
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.SSL_VERIFYHOST, False)
        #c.setopt(pycurl.ENCODING, 'gzip')
        c.setopt(pycurl.FORBID_REUSE, 0)
        c.setopt(c.URL, hstUrl)
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/json', 'Content-Type: application/json', 'charset=UTF-8'])
        #postfields = urlencode(post_data).encode('utf-8')  #表单数据编码
        postfields = urllib.parse.urlencode(post_data)
        print("postfields = ", postfields)
        #c.setopt(pycurl.POST, len(postfields))
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.POSTFIELDS, postfields) #POSTFIELDS自动以POST的方式提交并请求发送数据
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        body=buffer.getvalue().decode()  #读取缓存中的资源并解码
        print(body)

    #试图使用pycurl方案，没成功        
    #需要导入证书根证书集合
    def hstPycurlSecurityPost(self):
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL,'http://localhost:7999/')
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.CAINFO, certifi.where()) #设置指定证书验证包
        c.perform()
        c.close()
        body=buffer.getvalue()
        print(body.decode('utf-8'))        

    #试图使用http方案，没成功    
    def hstHttpPost(self):   
        #connection = http.client.HTTPConnection('http://localhost:7999/')
        connection = ''
        headers = {'Content-type': 'application/json'}
        values = {
            'acct_pan':'6226011****83678',
            'acct_name':'张三',
            'cert_type':'01',
            'cert_id':'37293019****95',
            'phone_num':'1516××××02'
        }
        json_foo = json.dumps(values)
        #connection.request('POST', '/authen/verifi?access_token=e2011a', json_foo, headers)
        connection.request('POST', '', json_foo, headers)
        response = connection.getresponse()
        print(response.read().decode())




#业务处理类，继承基类的属性
# class TupClsHstapi(TupClsHstapiBasic):
#     '''
#     classdocs
#     '''
# 
#     _TUP_HST_MSG_MATRIX = [\
#         {'restTag':'dba', 'actionId':3800, 'actionName':'opr_env', 'comments':''},\
#         {'restTag':'dba', 'actionId':3801, 'actionName':'opr_counter', 'comments':''},\
#         {'restTag':'dba', 'actionId':3802, 'actionName':'opr_fspc', 'comments':''},\
#         {'restTag':'dba', 'actionId':3803, 'actionName':'opr_file', 'comments':''},\
#         ]
#     
#     def __init__(self):
#         '''
#         Constructor
#         '''
#     
#     #初始化表单
#     def hstapiEnvInit(self, tupLable):
#         searchFlag = False
#         for element in self._TUP_HST_MSG_MATRIX:
#             if element['actionName'] == 'opr_env':
#                 searchFlag = True
#                 actionId = element['actionId']
#         if (searchFlag == False):
#             return -1, ''
#         inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'init', 'tupLable':tupLable})
#         res = self.hstCurlPost(inputJson)
#         restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
#         if (restTag != 'dba'):
#             return -2, ''
#         if (newActionId != actionId):
#             return -3, ''
#         if (parFlag <= 0):
#             return -4, ''
#         return 1, parContent
# 
#     #更新表单
#     def hstapiEnvUpdate(self, tupLable):
#         searchFlag = False
#         for element in self._TUP_HST_MSG_MATRIX:
#             if element['actionName'] == 'opr_env':
#                 searchFlag = True
#                 actionId = element['actionId']
#         if (searchFlag == False):
#             return -1, ''
#         inputJson = self.hstapiEncode('dba', actionId, True, {'cmd':'add', 'tupLable':tupLable})
#         res = self.hstCurlPost(inputJson)
#         restTag, newActionId, parFlag, parContent = self.hstapiDecode(res)
#         if (restTag != 'dba'):
#             return -2, ''
#         if (newActionId != actionId):
#             return -3, ''
#         if (parFlag <= 0):
#             return -4, ''
#         return 1, parContent        
# 
#     
#     
#     
# 
# 
# 
# if __name__ == '__main__':
#     cls = TupClsHstapi()
#     #res = hst.hstCurlPost({"restTag": "dba", "actionId": 3800, "parFlag": 1, "parContent":{"cmd":"add","user":"test222"}})
#     print(cls.hstapiEnvInit('test'))
#     print(cls.hstapiEnvUpdate('test'))


















