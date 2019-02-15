'''
Created on 2019/2/14

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
import paho.mqtt.client as mqtt
from multiprocessing import Queue, Process
import threading





class TupClsHuicobusBasic(object):
    '''
    classdocs
    '''
    _TUP_MQTT_SVR = ''
    
    def __init__(self):
        '''
        Constructor
        '''
        self._TUP_MQTT_SVR = TupClsMqttThread()

    def data_send(self):
        pass


        
        
#MQTT服务任务        
class TupClsMqttThread():
    _TUP_MQTT_HOST = ''
    _TUP_MQTT_PORT = ''
    
    def __init__(self):
        self._TUP_MQTT_HOST = None  #'localhost'  #'127.0.0.1'
        self._TUP_MQTT_PORT = 1883
        myThread = threading.Thread(target=self.handler_server, args=())
        myThread.start()
            
    def handler_server(self):
        client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        client = mqtt.Client(client_id)    # ClientId不能重复，所以使用当前时间
        client.username_pw_set("admin", "123456")  # 必须设置，否则会返回「Connected with result code 4」
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self._TUP_MQTT_HOST, port = self._TUP_MQTT_PORT, keepalive = 60)
        client.loop_forever()
        
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("chat")

    def on_message(self, client, userdata, msg):
        print(msg.topic+" " + ":" + str(msg.payload))

     
    #客户端测试        
    HOST = "127.0.0.1"
    PORT = 1883
    def client_test(self):
        client = mqtt.Client()
        client.connect(self.HOST, self.PORT, 60)
        client.publish("chat","hello chenfulin",2)
        client.loop_forever()        
        
        
    
if __name__ == '__main__':
    cls = TupClsHuicobusBasic()















        
        
        
        
        