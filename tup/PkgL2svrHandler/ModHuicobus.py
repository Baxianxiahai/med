'''
Created on 2019/2/14

@author: Administrator
'''

#import random
#import sys
#import time
#import os
#import re
#import urllib
#import http
#import socket
#import datetime
#import string
#import ctypes 
#import cv2 as cv
#import numpy as np
#import matplotlib.pyplot as plt
#import math
#from   ctypes import c_uint8
#import urllib
#import urllib3
#import requests
#import socket
#import pycurl
#import io
#import certifi  #导入根证书集合，用于验证SSL证书可信和TLS主机身份
#from io import BytesIO
#from urllib.parse import urlencode
#import http.client
#from multiprocessing import Queue, Process
#import threading
#from multiprocessing import Queue, Process
import json
import paho.mqtt.client as mqtt
from PkgL1vmHandler.ModVmCfg import *
from PkgL1vmHandler.ModVmLayer import *
from PkgL1vmHandler.ModVmConsole import *



HOST = "127.0.0.1"
PORT = 1883

#基类
class TupClsHuicobusBasic(tupTaskTemplate):
    '''
    classdocs
    '''
    _STM_ACTIVE = 3
    _STM_DEACT  = 4
    _TUP_MQTT_SVR = '127.0.0.1'
    _TUP_MQTT_HOST = 1883
    _TUP_UP_LAYER = 0


    #固定定义-节点
    _HUICOBUS_MQTT_NBID_MIN = 0
    _HUICOBUS_MQTT_NBID_LOCALHOST = 1       #本机
    _HUICOBUS_MQTT_NBID_ECCSERVER = 2        #ECC服务器
    _HUICOBUS_MQTT_NBID_FACSERVER = 3        #本地服务器
    _HUICOBUS_MQTT_NBID_REMSERVER = 4        #远程服务器
    _HUICOBUS_MQTT_NBID_MATINC = 5            #进料控制机
    _HUICOBUS_MQTT_NBID_TUPSVR = 6            #TUP服务节点
    _HUICOBUS_MQTT_NBID_TUPCLT = 7            #TUP控制客户节点
    _HUICOBUS_MQTT_NBID_MAX = 8
    _HUICOBUS_MQTT_NBID_INVALID = 0xFFFFFFFF
    _HUICOBUS_MQTT_NBID = ('HUICOBUS_MQTT_NODEID_MIN',\
                        'HUICOBUS_MQTT_NODEID_LOCALHOST',\
                        'HUICOBUS_MQTT_NODEID_ECCSERVER',\
                        'HUICOBUS_MQTT_NODEID_FACSERVER',\
                        'HUICOBUS_MQTT_NODEID_REMSERVER',\
                        'HUICOBUS_MQTT_NODEID_MATINC',\
                        'HUICOBUS_MQTT_NODEID_TUPSVR',\
                        'HUICOBUS_MQTT_NODEID_TUPCLT',\
                        'HUICOBUS_MQTT_NODEID_MAX',\
                        )
    
    #固定定义-客户ID
    _HUICOBUS_MQTT_CLID_MIN = 0
    _HUICOBUS_MQTT_CLID_HCUENTRY = 1        #工控机主题控制器
    _HUICOBUS_MQTT_CLID_UIROUTER = 2        #PHP为基础的控制界面业务逻辑
    _HUICOBUS_MQTT_CLID_UIPRESENT = 3        #触屏UI界面
    _HUICOBUS_MQTT_CLID_QRPRINTER = 4        #打印机
    _HUICOBUS_MQTT_CLID_DBRESTFUL = 5        #数据库
    _HUICOBUS_MQTT_CLID_BHPROTO = 6            #回传协议
    _HUICOBUS_MQTT_CLID_LOGERR = 7            #差错log
    _HUICOBUS_MQTT_CLID_LOGTRACE = 8        #调测打印log
    _HUICOBUS_MQTT_CLID_OPRNODE = 9            #操控控制节点，即为控制服务器
    _HUICOBUS_MQTT_CLID_ECCTV = 10              #ECC广播
    _HUICOBUS_MQTT_CLID_TUPENTRY = 11        #TUP业务控制者
    _HUICOBUS_MQTT_CLID_TUPROUTER = 12       #PHP路由器
    _HUICOBUS_MQTT_CLID_H5UI = 13                #H5UI的远程页面控制界面
    _HUICOBUS_MQTT_CLID_MAX = 14
    _HUICOBUS_MQTT_CLID_INVALID = 0xFFFFFFFF
    _HUICOBUS_MQTT_CLID = ('HUICOBUS_MQTT_CLIENTID_MIN',\
                        'HUICOBUS_MQTT_CLIENTID_HCUENTRY',\
                        'HUICOBUS_MQTT_CLIENTID_UIROUTER',\
                        'HUICOBUS_MQTT_CLIENTID_UIPRESENT',\
                        'HUICOBUS_MQTT_CLIENTID_QRPRINTER',\
                        'HUICOBUS_MQTT_CLIENTID_DBRESTFUL',\
                        'HUICOBUS_MQTT_CLIENTID_BHPROTO',\
                        'HUICOBUS_MQTT_CLIENTID_LOGERR',\
                        'HUICOBUS_MQTT_CLIENTID_LOGTRACE',\
                        'HUICOBUS_MQTT_CLIENTID_OPRNODE',\
                        'HUICOBUS_MQTT_CLIENTID_ECCTV',\
                        'HUICOBUS_MQTT_CLIENTID_TUPENTRY',\
                        'HUICOBUS_MQTT_CLIENTID_TUPROUTER',\
                        'HUICOBUS_MQTT_CLIENTID_H5UI',\
                        'HUICOBUS_MQTT_CLIENTID_MAX',\
                        )
    
    #固定定义-频道ID
    _HUICOBUS_MQTT_TPID_MIN = 0
    _HUICOBUS_MQTT_TPID_HCU2UIR = 1
    _HUICOBUS_MQTT_TPID_UIR2HCU = 2
    _HUICOBUS_MQTT_TPID_UIR2UIP = 3
    _HUICOBUS_MQTT_TPID_PRINTFLOW = 4
    _HUICOBUS_MQTT_TPID_DBACCESS = 5
    _HUICOBUS_MQTT_TPID_DBFEEDBACK = 6
    _HUICOBUS_MQTT_TPID_BHTRANS = 7
    _HUICOBUS_MQTT_TPID_LOGERRFLOW = 8
    _HUICOBUS_MQTT_TPID_LOGTRACEFLOW = 9
    _HUICOBUS_MQTT_TPID_HCU2OPN = 10
    _HUICOBUS_MQTT_TPID_OPN2HCU = 11
    _HUICOBUS_MQTT_TPID_ECCTV2HCU = 12      #广播过程，向所有设备广播每一台设备的标签、路由地址、角色
    _HUICOBUS_MQTT_TPID_HCU2ECCARP = 13     #模拟反向解析指令，获取每一个网关设备的标签，并知晓死活
    _HUICOBUS_MQTT_TPID_TUP2UIR = 14        #TUP发送给UIR的命令
    _HUICOBUS_MQTT_TPID_UIR2TUP = 15        #UIR发送给TUP的命令
    _HUICOBUS_MQTT_TPID_UIR2H5UI = 16       #UIR发送给H5UI的命令
    _HUICOBUS_MQTT_TPID_MAX = 17
    _HUICOBUS_MQTT_TPID_INVALID = 0xFFFFFFFF
    _HUICOBUS_MQTT_TPID = ('HUICOBUS_MQTT_TOPIC_MIN',\
                        'HUICOBUS_MQTT_TOPIC_HCU2UIR',\
                        'HUICOBUS_MQTT_TOPIC_UIR2HCU',\
                        'HUICOBUS_MQTT_TOPIC_UIR2UIP',\
                        'HUICOBUS_MQTT_TOPIC_PRINTFLOW',\
                        'HUICOBUS_MQTT_TOPIC_DBACCESS',\
                        'HUICOBUS_MQTT_TOPIC_DBFEEDBACK',\
                        'HUICOBUS_MQTT_TOPIC_BHTRANS',\
                        'HUICOBUS_MQTT_TOPIC_LOGERRFLOW',\
                        'HUICOBUS_MQTT_TOPIC_LOGTRACEFLOW',\
                        'HUICOBUS_MQTT_TOPIC_HCU2OPN',\
                        'HUICOBUS_MQTT_TOPIC_OPN2HCU',\
                        'HUICOBUS_MQTT_TOPIC_ECCTV2HCU',\
                        'HUICOBUS_MQTT_TOPIC_HCU2ECCARP',\
                        'HUICOBUS_MQTT_TOPIC_TUP2UIR',\
                        'HUICOBUS_MQTT_TOPIC_UIR2TUP',\
                        'HUICOBUS_MQTT_TOPIC_UIR2H5UI',\
                        'HUICOBUS_MQTT_TOPIC_MAX',\
                        )
    
    _TUP_HUIJSON_MSG_MATRIX = [\
        {'topic':'HUICOBUS_MQTT_TOPIC_TUP2UIR', 'cmdId':0x0A00, 'cmdName':'HUICOBUS_CMDID_cui_tup2uir_ctrl_req', 'msgId':TUP_MSGID_HUICOBUS_CTRL_REQ, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_TUP2UIR', 'cmdId':0x0A01, 'cmdName':'HUICOBUS_CMDID_cui_tup2uir_ctrl_confirm', 'msgId':TUP_MSGID_HUICOBUS_CTRL_CONFIRM, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_TUP2UIR', 'cmdId':0x0A02, 'cmdName':'HUICOBUS_CMDID_cui_tup2uir_moto_confirm', 'msgId':TUP_MSGID_HUICOBUS_MOTO_CONFIRM, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_TUP2UIR', 'cmdId':0x0A03, 'cmdName':'HUICOBUS_CMDID_cui_tup2uir_cam_confirm', 'msgId':TUP_MSGID_HUICOBUS_CAM_CONFIRM, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_TUP2UIR', 'cmdId':0x0A04, 'cmdName':'HUICOBUS_CMDID_cui_tup2uir_calib_confirm', 'msgId':TUP_MSGID_HUICOBUS_CALIB_CONFIRM, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_TUP2UIR', 'cmdId':0x0A05, 'cmdName':'HUICOBUS_CMDID_cui_tup2uir_test_cmd_confirm', 'msgId':TUP_MSGID_HUICOBUS_TEST_CMD_CONFIRM, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_TUP2UIR', 'cmdId':0x0A06, 'cmdName':'HUICOBUS_CMDID_cui_tup2uir_cfy_confirm', 'msgId':TUP_MSGID_HUICOBUS_CFY_CONFIRM, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_TUP2UIR', 'cmdId':0x0A07, 'cmdName':'HUICOBUS_CMDID_cui_tup2uir_notify', 'msgId':TUP_MSGID_HUICOBUS_NOTIFY, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_UIR2TUP', 'cmdId':0x0A80, 'cmdName':'HUICOBUS_CMDID_cui_uir2tup_ctrl_resp', 'msgId':TUP_MSGID_HUICOBUS_CTRL_RESP, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_UIR2TUP', 'cmdId':0x0A81, 'cmdName':'HUICOBUS_CMDID_cui_uir2tup_ctrl_report', 'msgId':TUP_MSGID_HUICOBUS_CTRL_REPORT, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_UIR2TUP', 'cmdId':0x0A82, 'cmdName':'HUICOBUS_CMDID_cui_uir2tup_moto_report', 'msgId':TUP_MSGID_HUICOBUS_MOTO_REPORT, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_UIR2TUP', 'cmdId':0x0A83, 'cmdName':'HUICOBUS_CMDID_cui_uir2tup_cam_report', 'msgId':TUP_MSGID_HUICOBUS_CAM_REPORT, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_UIR2TUP', 'cmdId':0x0A84, 'cmdName':'HUICOBUS_CMDID_cui_uir2tup_calib_report', 'msgId':TUP_MSGID_HUICOBUS_CALIB_REPORT, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_UIR2TUP', 'cmdId':0x0A85, 'cmdName':'HUICOBUS_CMDID_cui_uir2tup_test_cmd_report', 'msgId':TUP_MSGID_HUICOBUS_TEST_CMD_REPORT, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_UIR2TUP', 'cmdId':0x0A86, 'cmdName':'HUICOBUS_CMDID_cui_uir2tup_cfy_report', 'msgId':TUP_MSGID_HUICOBUS_CFY_REPORT, 'comments':''},\
        ]


    def __init__(self, taskidUb, taskNameUb, glParUb):
        tupTaskTemplate.__init__(self, taskid=taskidUb, taskName=taskNameUb, glTabEntry=glParUb)
        self.fsm_set(TUP_STM_NULL)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_com_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_EXIT, self.fsm_com_msg_exit_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TEST, self.fsm_com_msg_test_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_HUICOBUS_REG_UP_USER, self.fsm_reg_up_user_rcv_handler)
        #业务处理部分
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_HUICOBUS_CTRL_REQ, self.fsm_msg_ctrl_req_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_HUICOBUS_CTRL_CONFIRM, self.fsm_msg_ctrl_confirm_rcv_handler)
    
    '''
    #
    #模块初始化
    #
    '''
    def fsm_msg_init_rcv_handler(self, msgContent):
        self._TUP_MQTT_SVR = TupClsMqttThread(self, self._TUP_MQTT_SVR, self._TUP_MQTT_HOST)
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;
    
    def fsm_reg_up_user_rcv_handler(self, msgContent):
        self._TUP_UP_LAYER = msgContent['userTaskId']
        return TUP_SUCCESS;
    
    #基础调用函数
    def func_data_send(self, jsonInput):
        client = mqtt.Client()
        client.connect(HOST, PORT, 60)
        client.publish(self._HUICOBUS_MQTT_TPID[self._HUICOBUS_MQTT_TPID_TUP2UIR], json.dumps(jsonInput), 2)
        
    #函数原型，等待被业务层所重载
    #UIR send to TUP HUICOBUS message
    def func_data_rcv(self, cmdId, cmdValue, hlContent):
        #print("I receive cmdId = ", cmdId, 'cmdValue = ', cmdValue, 'ParContent = ', str(hlContent))
        mbuf = {}
        mbuf['cmdValue'] = cmdValue
        mbuf['hlContent'] = hlContent
        msgId = 0
        for element in self._TUP_HUIJSON_MSG_MATRIX:
            if (element['topic'] == 'HUICOBUS_MQTT_TOPIC_UIR2TUP') and (element['cmdId'] == cmdId):
                msgId = element['msgId']
        if (self._TUP_UP_LAYER != 0):
            self.msg_send(msgId, self._TUP_UP_LAYER, mbuf)
        return

    '''
    #
    #SERVICE PROCESSING
    #
    '''
    def fsm_msg_ctrl_req_rcv_handler(self, msgContent):
        jsonInput = {}
        jsonInput['srcNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
        jsonInput['destNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
        jsonInput['srcId'] = 'HUICOBUS_MQTT_CLIENTID_TUPENTRY'
        jsonInput['destId'] = 'HUICOBUS_MQTT_CLIENTID_TUPROUTER'
        jsonInput['topicId'] = 'HUICOBUS_MQTT_TOPIC_TUP2UIR'
        jsonInput['cmdId'] = 0
        for element in self._TUP_HUIJSON_MSG_MATRIX:
            if (element['topic'] == jsonInput['topicId']) and (element['cmdName'] == 'HUICOBUS_CMDID_cui_tup2uir_ctrl_req'):
                jsonInput['cmdId'] = element['cmdId']
        jsonInput['cmdValue'] = msgContent['cmdValue']
        jsonInput['hlContent'] = msgContent['hlContent']
        self.func_data_send(jsonInput)
        return TUP_SUCCESS

    def fsm_msg_ctrl_confirm_rcv_handler(self, msgContent):
        jsonInput = {}
        jsonInput['srcNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
        jsonInput['destNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
        jsonInput['srcId'] = 'HUICOBUS_MQTT_CLIENTID_TUPENTRY'
        jsonInput['destId'] = 'HUICOBUS_MQTT_CLIENTID_TUPROUTER'
        jsonInput['topicId'] = 'HUICOBUS_MQTT_TOPIC_TUP2UIR'
        jsonInput['cmdId'] = 0
        for element in self._TUP_HUIJSON_MSG_MATRIX:
            if (element['topic'] == jsonInput['topicId']) and (element['cmdName'] == 'HUICOBUS_CMDID_cui_tup2uir_ctrl_confirm'):
                jsonInput['cmdId'] = element['cmdId']
        jsonInput['cmdValue'] = msgContent['cmdValue']
        jsonInput['hlContent'] = msgContent['hlContent']
        self.func_data_send(jsonInput)
        return TUP_SUCCESS

    #客户端测试 - 这个是模拟H5UI发送到TUP实体的      
    def client_test(self, jsonInput):
        client = mqtt.Client()
        client.connect(HOST, PORT, 60)
        client.publish("HUICOBUS_MQTT_TOPIC_UIR2TUP", json.dumps(jsonInput), 2)

#MQTT服务任务
class TupClsMqttThread():
    def __init__(self, father, svrAddr, svrPort):
        self.father = father
        self.svrAddr = svrAddr
        self.svrPort = svrPort
        myThread = threading.Thread(target=self.handler_server, args=())
        myThread.start()
            
    def handler_server(self):
        client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        client = mqtt.Client(client_id)    # ClientId不能重复，所以使用当前时间
        client.username_pw_set("admin", "123456")  # 必须设置，否则会返回「Connected with result code 4」
        client.on_connect = self.func_on_connect
        client.on_message = self.func_on_message
        client.connect(self.svrAddr, port = self.svrPort, keepalive = 60)
        client.loop_forever()
    
    #连接事件    
    def func_on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(self._HUICOBUS_MQTT_TPID[self._HUICOBUS_MQTT_TPID_UIR2TUP])
    
    #收到数据，这里采用回调的方式
    def func_on_message(self, client, userdata, msg):
        #print(msg.topic+" " + ":" + str(msg.payload))
        #解码固定消息头
        try:
            r = json.loads(msg.payload)
        except Exception:
            pass
        if ('srcNode' not in r) or ('destNode' not in r) or ('srcId' not in r) or ('destId' not in r) or ('topicId' not in r) or ('cmdId' not in r) or ('cmdValue' not in r) or ('hlContent' not in r):
            print("Error -1")
            return -1
        srcNode = r['srcNode']
        if (srcNode != self._HUICOBUS_MQTT_NBID[self._HUICOBUS_MQTT_NBID_TUPSVR]):
            print("Error -2")
            return -2
        destNode = r['destNode']
        if (destNode != self._HUICOBUS_MQTT_NBID[self._HUICOBUS_MQTT_NBID_TUPSVR]):
            print("Error -3")
            return -3
        srcId = r['srcId']
        if (srcId != self._HUICOBUS_MQTT_CLID[self._HUICOBUS_MQTT_CLID_TUPROUTER]):
            print("Error -4")
            return -4
        destId = r['destId']
        if (destId != self._HUICOBUS_MQTT_CLID[self._HUICOBUS_MQTT_CLID_TUPENTRY]):
            print("Error -5")
            return -5
        topicId = r['topicId']
        if (topicId != self._HUICOBUS_MQTT_TPID[self._HUICOBUS_MQTT_TPID_UIR2TUP]):
            print("Error -6, topicid=", topicId)
            return -6
        cmdId = r['cmdId']
        cmdFlag = False
        for element in self._TUP_HUIJSON_MSG_MATRIX:
            if (element['cmdId'] == cmdId) and (element['topic'] == topicId):
                cmdFlag = True
        if (cmdFlag == False):
            print("Error -7")
            return -7
        cmdValue = r['cmdValue']
        hlContent = r['hlContent']
        self.father.func_data_rcv(cmdId, cmdValue, hlContent)
        return 1

        
    
if __name__ == '__main__':
    #创建并初始化
    TUP_GL_CFG = tupGlbCfg()
    initMsg = {}
    initMsg['mid'] = TUP_MSGID_INIT
    initMsg['src'] = TUP_TASK_ID_TUPCONSL
    initMsg['content'] = ""
    cls = TupClsHuicobusBasic(TUP_TASK_ID_HUICOBUS, "TASK_HUICOBUS", TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_HUICOBUS
    cls.msg_send_in(initMsg)
    cls.tup_dbg_print("Create HUICOBUS task success!")
    #注册上层应用模块
    initMsg['mid'] = TUP_MSGID_HUICOBUS_REG_UP_USER
    mbuf = {}
    mbuf['userTaskId'] = TUP_TASK_ID_UI_GPAR
    initMsg['content'] = mbuf
    cls.msg_send_in(initMsg)
    cls.func_data_send({'test':1})
    time.sleep(1)
    cls.client_test({'srcNode':'HUICOBUS_MQTT_NODEID_TUPSVR', \
                'destNode':'HUICOBUS_MQTT_NODEID_TUPSVR', \
                'srcId':'HUICOBUS_MQTT_CLIENTID_TUPROUTER', \
                'destId':'HUICOBUS_MQTT_CLIENTID_TUPENTRY', \
                'topicId':'HUICOBUS_MQTT_TOPIC_UIR2TUP', \
                'cmdId':2689, \
                'cmdValue':123, \
                'hlContent':{'a':1, 'b':2}\
                })














        
        
        
        
        