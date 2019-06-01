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
import paho.mqtt.publish as publish
from PkgL1vmHandler.ModSysConfig import *
from PkgL1vmHandler.ModVmCfg import *
from PkgL1vmHandler.ModVmLayer import *
from PkgL1vmHandler.ModVmConsole import *


class ClassJoinContents:
    def __init__(self):
        self.contents = ''
    def callback(self,curl):
        self.contents = self.contents + curl.decode('utf-8')
    
def cebs_huicobus_msg_send(jsonInput):
    tmpClientId = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    publish.single("HUICOBUS_MQTT_TOPIC_UIP2TUP", json.dumps(jsonInput), qos = 2, keepalive=1, hostname="127.0.0.1", port=1883, client_id=tmpClientId, auth = {'username':"admin", 'password':"123456"})

    
    
    
    
    