'''
Created on 2019年5月31日

@author: Administrator
'''

import urllib
import json
import time
import urllib3
import requests
import socket
from PkgL2svrUniv.ModCebsHuicobus import *
import json
import paho.mqtt.client as mqtt
from PkgL1vmHandler.ModSysConfig import *
from PkgL1vmHandler.ModVmCfg import *
from PkgL1vmHandler.ModVmLayer import *
from PkgL1vmHandler.ModVmConsole import *
import paho.mqtt.client as mqtt


class ClassJoinContents:
    def __init__(self):
        self.contents = ''
    def callback(self,curl):
        self.contents = self.contents + curl.decode('utf-8')
    
def cebs_huicobus_msg_send(msg):
#     TUP_GL_CFG = tupGlbCfg()
#     cls = TupClsCebsHuicobusItf(TUP_GL_CFG);
#     initMsg = {}
#     initMsg['mid'] = TUP_MSGID_INIT
#     initMsg['src'] = TUP_TASK_ID_TUPCONSL
#     initMsg['dst'] = TUP_TASK_ID_HUICOBUS
#     mbuf={}
#     mbuf['uplayer'] = TUP_TASK_ID_HUICOBUS
#     initMsg['content'] = mbuf
#     cls.msg_send_in(initMsg)
#     time.sleep(0.001)
#     cls.client_test(msg)
    client = mqtt.Client()
    client.connect(TUP_HUICOBUS_MQTT_HOST, TUP_HUICOBUS_MQTT_PORT, 60)
    client.publish("HUICOBUS_MQTT_TOPIC_UIP2TUP", json.dumps(msg), 0)

    
    
    
    
    
    