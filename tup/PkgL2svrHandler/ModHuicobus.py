'''
Created on 2019/2/14

@author: Administrator
'''
import json
import sys
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from PkgL1vmHandler.ModSysConfig import *
from PkgL1vmHandler.ModVmCfg import *
from PkgL1vmHandler.ModVmLayer import *
from PkgL1vmHandler.ModVmConsole import *
from PkgL2svrHandler.headHuicobus import *

import logging
logging.basicConfig(level=logging.INFO)


#基类
class TupClsHuicobusBasic(tupTaskTemplate):
    '''
    classdocs
    '''
    _STM_ACTIVE = 3
    _STM_DEACT  = 4
    
    _TUP_MQTT_SVR = 0
    _TUP_MQTT_HOST = 0
    _TUP_MQTT_PORT = 0
    _TUP_UP_LAYER = 0


    #固定定义-节点
    _HUICOBUS_MQTT_NBID_MIN = 0
    _HUICOBUS_MQTT_NBID_LOCALHOST = 1           #本机
    _HUICOBUS_MQTT_NBID_ECCSERVER = 2           #ECC服务器
    _HUICOBUS_MQTT_NBID_FACSERVER = 3           #本地服务器
    _HUICOBUS_MQTT_NBID_REMSERVER = 4           #远程服务器
    _HUICOBUS_MQTT_NBID_MATINC = 5              #进料控制机
    _HUICOBUS_MQTT_NBID_TUPSVR = 6              #TUP服务节点
    _HUICOBUS_MQTT_NBID_TUPCLT = 7              #TUP控制客户节点
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
    _HUICOBUS_MQTT_CLID_UIPRESENT = 3       #触屏UI界面
    _HUICOBUS_MQTT_CLID_QRPRINTER = 4       #打印机
    _HUICOBUS_MQTT_CLID_DBRESTFUL = 5       #数据库
    _HUICOBUS_MQTT_CLID_BHPROTO = 6         #回传协议
    _HUICOBUS_MQTT_CLID_LOGERR = 7          #差错log
    _HUICOBUS_MQTT_CLID_LOGTRACE = 8        #调测打印log
    _HUICOBUS_MQTT_CLID_OPRNODE = 9         #操控控制节点，即为控制服务器
    _HUICOBUS_MQTT_CLID_ECCTV = 10          #ECC广播
    _HUICOBUS_MQTT_CLID_TUPENTRY = 11       #TUP业务控制者
    _HUICOBUS_MQTT_CLID_TUPROUTER = 12      #PHP路由器
    _HUICOBUS_MQTT_CLID_H5UI = 13           #H5UI的远程页面控制界面
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
    _HUICOBUS_MQTT_TPID_TUP2UIP = 14        #TUP发送给UIP的命令
    _HUICOBUS_MQTT_TPID_UIP2TUP = 15        #UIP发送给TUP的命令
    _HUICOBUS_MQTT_TPID_UIP2H5UI = 16       #UIP发送给H5UI的命令
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
                        'HUICOBUS_MQTT_TOPIC_TUP2UIP',\
                        'HUICOBUS_MQTT_TOPIC_UIP2TUP',\
                        'HUICOBUS_MQTT_TOPIC_UIP2H5UI',\
                        'HUICOBUS_MQTT_TOPIC_MAX',\
                        )
    
    _TUP_HUICOBUS_MSG_MATRIX = [\
        {'topic':'HUICOBUS_MQTT_TOPIC_UIP2TUP', 'cmdId':TUP_HHD_CMDID_SYS_GET_CONFIG_REQ, 'cmdName':'HUICOBUS_CMDID_cui_tup2uip_get_cfg_req', 'msgId':TUP_MSGID_HUICOBUS_GET_CFG_REQ, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_TUP2UIP', 'cmdId':TUP_HHD_CMDID_SYS_GET_CONFIG_RESP, 'cmdName':'HUICOBUS_CMDID_cui_uip2tup_get_cfg_resp', 'msgId':TUP_MSGID_HUICOBUS_GET_CFG_RESP, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_UIP2TUP', 'cmdId':TUP_HHD_CMDID_SYS_SET_CONFIG_REQ, 'cmdName':'HUICOBUS_CMDID_cui_tup2uip_set_cfg_req', 'msgId':TUP_MSGID_HUICOBUS_SET_CFG_REQ, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_TUP2UIP', 'cmdId':TUP_HHD_CMDID_SYS_SET_CONFIG_RESP, 'cmdName':'HUICOBUS_CMDID_cui_uip2tup_set_cfg_resp', 'msgId':TUP_MSGID_HUICOBUS_SET_CFG_RESP, 'comments':''},\

        {'topic':'HUICOBUS_MQTT_TOPIC_TUP2UIP', 'cmdId':0x0A10, 'cmdName':'HUICOBUS_CMDID_cui_tup2uip_ctrl_req', 'msgId':TUP_MSGID_HUICOBUS_CTRL_REQ, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_TUP2UIP', 'cmdId':0x0A11, 'cmdName':'HUICOBUS_CMDID_cui_tup2uip_ctrl_confirm', 'msgId':TUP_MSGID_HUICOBUS_CTRL_CONFIRM, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_TUP2UIP', 'cmdId':0x0A12, 'cmdName':'HUICOBUS_CMDID_cui_tup2uip_moto_confirm', 'msgId':TUP_MSGID_HUICOBUS_MOTO_CONFIRM, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_TUP2UIP', 'cmdId':0x0A13, 'cmdName':'HUICOBUS_CMDID_cui_tup2uip_cam_confirm', 'msgId':TUP_MSGID_HUICOBUS_CAM_CONFIRM, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_TUP2UIP', 'cmdId':0x0A14, 'cmdName':'HUICOBUS_CMDID_cui_tup2uip_calib_confirm', 'msgId':TUP_MSGID_HUICOBUS_CALIB_CONFIRM, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_TUP2UIP', 'cmdId':0x0A15, 'cmdName':'HUICOBUS_CMDID_cui_tup2uip_test_cmd_confirm', 'msgId':TUP_MSGID_HUICOBUS_TEST_CMD_CONFIRM, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_TUP2UIP', 'cmdId':0x0A16, 'cmdName':'HUICOBUS_CMDID_cui_tup2uip_cfy_confirm', 'msgId':TUP_MSGID_HUICOBUS_CFY_CONFIRM, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_TUP2UIP', 'cmdId':0x0A17, 'cmdName':'HUICOBUS_CMDID_cui_tup2uip_notify', 'msgId':TUP_MSGID_HUICOBUS_NOTIFY, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_UIP2TUP', 'cmdId':0x0A90, 'cmdName':'HUICOBUS_CMDID_cui_uip2tup_ctrl_resp', 'msgId':TUP_MSGID_HUICOBUS_CTRL_RESP, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_UIP2TUP', 'cmdId':0x0A91, 'cmdName':'HUICOBUS_CMDID_cui_uip2tup_ctrl_report', 'msgId':TUP_MSGID_HUICOBUS_CTRL_REPORT, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_UIP2TUP', 'cmdId':0x0A92, 'cmdName':'HUICOBUS_CMDID_cui_uip2tup_moto_report', 'msgId':TUP_MSGID_HUICOBUS_MOTO_REPORT, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_UIP2TUP', 'cmdId':0x0A93, 'cmdName':'HUICOBUS_CMDID_cui_uip2tup_cam_report', 'msgId':TUP_MSGID_HUICOBUS_CAM_REPORT, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_UIP2TUP', 'cmdId':0x0A94, 'cmdName':'HUICOBUS_CMDID_cui_uip2tup_calib_report', 'msgId':TUP_MSGID_HUICOBUS_CALIB_REPORT, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_UIP2TUP', 'cmdId':0x0A95, 'cmdName':'HUICOBUS_CMDID_cui_uip2tup_test_cmd_report', 'msgId':TUP_MSGID_HUICOBUS_TEST_CMD_REPORT, 'comments':''},\
        {'topic':'HUICOBUS_MQTT_TOPIC_UIP2TUP', 'cmdId':0x0A96, 'cmdName':'HUICOBUS_CMDID_cui_uip2tup_cfy_report', 'msgId':TUP_MSGID_HUICOBUS_CFY_REPORT, 'comments':''},\
        ]


    def __init__(self, taskidUb, taskNameUb, glParUb):
        tupTaskTemplate.__init__(self, taskid=taskidUb, taskName=taskNameUb, glTabEntry=glParUb)
        self._TUP_MQTT_HOST = TUP_HUICOBUS_MQTT_HOST
        self._TUP_MQTT_PORT = TUP_HUICOBUS_MQTT_PORT
        self.fsm_set(TUP_STM_NULL)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_com_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_EXIT, self.fsm_com_msg_exit_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TEST, self.fsm_com_msg_test_rcv_handler)
        #业务处理部分
        #Nothing
    
    '''
    #
    #模块初始化
    #
    '''
    def fsm_msg_init_rcv_handler(self, msgContent):
        self._TUP_MQTT_SVR = TupClsMqttThread(self, self._TUP_MQTT_HOST, self._TUP_MQTT_PORT)
        self.mqttclient=self._TUP_MQTT_SVR.func_get_mqtt_client()
        self._TUP_UP_LAYER = msgContent['uplayer']
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;


    '''
    #
    #发送接收基础函数
    #
    '''    
    #基础调用函数
    def func_data_send(self, jsonInput):
        client = mqtt.Client()
        client.connect(self._TUP_MQTT_HOST, self._TUP_MQTT_PORT, 60)
        client.publish(self._HUICOBUS_MQTT_TPID[self._HUICOBUS_MQTT_TPID_TUP2UIP], json.dumps(jsonInput), 2)
    
    #第二种single的publish方法
    def func_data_send2(self, jsonInput):
        tmpClientId = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        publish.single(self._HUICOBUS_MQTT_TPID_TUP2UIP, \
                       json.dumps(jsonInput),\
                       qos = 2,\
                       hostname = self._TUP_MQTT_HOST,\
                       port = self._TUP_MQTT_PORT,\
                       client_id = tmpClientId,\
                       auth = {'username':"admin", 'password':"123456"})

    #消息发送通用函数
    def func_huicobus_msg_snd(self, cmdId, cmdValue, hlContent):
        jsonInput = {}
        jsonInput['srcNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
        jsonInput['destNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
        jsonInput['srcId'] = 'HUICOBUS_MQTT_CLIENTID_TUPENTRY'
        jsonInput['destId'] = 'HUICOBUS_MQTT_CLIENTID_TUPROUTER'
        jsonInput['topicId'] = 'HUICOBUS_MQTT_TOPIC_TUP2UIP'
        jsonInput['cmdId'] = 0
        jsonInput['cmdValue'] = cmdValue
        for element in self._TUP_HUICOBUS_MSG_MATRIX:
            if (element['topic'] == jsonInput['topicId']) and (element['cmdId'] == cmdId):
                jsonInput['cmdId'] = element['cmdId']
        if (jsonInput['cmdId'] == 0):
            print("HUICOBUS: Not set cmdId correctly!")
            return TUP_FAILURE
        jsonInput['hlContent'] = hlContent
        #print("HUICOBUS: Sending message = ", jsonInput)
        self.func_data_send(jsonInput)
        print("HUOCOBUS: Send accomplished! Content = ", jsonInput)
        return TUP_SUCCESS

        
    #函数原型，等待被业务层所重载
    #UIP send to TUP HUICOBUS message
    def func_data_rcv(self, cmdId, cmdValue, hlContent):
        mbuf = {}
        mbuf['cmdValue'] = cmdValue
        mbuf['hlContent'] = hlContent
        msgId = 0
        for element in self._TUP_HUICOBUS_MSG_MATRIX:
            if (element['topic'] == 'HUICOBUS_MQTT_TOPIC_UIP2TUP') and (element['cmdId'] == cmdId):
                msgId = element['msgId']
                continue
        if (self._TUP_UP_LAYER != 0):
            self.msg_send(msgId, self._TUP_UP_LAYER, mbuf)
        return TUP_SUCCESS

    #客户端测试 - 这个是模拟H5UI发送到TUP实体的      
    def client_publish_test(self, jsonInput):
        client = mqtt.Client()
        client.connect(self._TUP_MQTT_HOST, self._TUP_MQTT_PORT, 60)
        client.publish("HUICOBUS_MQTT_TOPIC_UIP2TUP", json.dumps(jsonInput), 2)


#MQTT服务任务
class TupClsMqttThread(TupClsHuicobusBasic):
    def __init__(self, father, svrAddr, svrPort):
        self.father = father
        self.svrAddr = svrAddr
        self.svrPort = svrPort
        client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.client = mqtt.Client(client_id)    #
        myThread = threading.Thread(target=self.handler_server, args=())
        myThread.start()
            
    def handler_server(self):
        self.client.username_pw_set("admin", "123456")  # 必须设置，否则会返回「Connected with result code 4」
        self.client.on_connect = self.func_on_connect
        self.client.on_message = self.func_on_message
        self.client.on_publish=self.func_on_publish
        #self.client.on_log=self.func_on_log
        self.client.on_disconnect=self.func_on_disconnect
        logger = logging.getLogger(__name__)
        self.client.enable_logger(logger)
        self.client.connect(self.svrAddr, port = self.svrPort, keepalive = 60)
        self.client.subscribe(self._HUICOBUS_MQTT_TPID[self._HUICOBUS_MQTT_TPID_UIP2TUP], qos=2)
        self.client.loop_forever()
    
    def func_get_mqtt_client(self):
        return self.client;

    def func_on_publish(self,client, userdata, mid):
        print(client, userdata, mid)
    
    #连接事件    
    def func_on_connect(self, client, userdata, flags, rc):
        client.subscribe(self._HUICOBUS_MQTT_TPID[self._HUICOBUS_MQTT_TPID_UIP2TUP], qos=2)

    def func_on_disconnect(self,client, userdata,rc=0):
        logging.debug("DisConnected result code "+str(rc))
        self.client.loop_stop()

    def func_on_log(self,client, userdata, level, buf):
        print("log: ",buf)
    
    #收到数据，这里采用回调的方式
    #r = json.loads(msg.payload.decode(encoding='utf-8'), strict=False)
    def func_on_message(self, client, userdata, msg):
        r = ''
        #解码固定消息头
        try:
            r = json.loads(msg.payload)
        except Exception:
            print("Rcv msg json decode error! Error cause = ", sys.exc_info()[0])
        if ('srcNode' not in r) or ('destNode' not in r) or ('srcId' not in r) or ('destId' not in r) or ('topicId' not in r) or ('cmdId' not in r) or ('cmdValue' not in r) or ('hlContent' not in r):
            print("Error -1, Rcv = ", r)
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
        if (topicId != self._HUICOBUS_MQTT_TPID[self._HUICOBUS_MQTT_TPID_UIP2TUP]):
            print("Error -6, topicid=", topicId)
            return -6
        cmdId = r['cmdId']
        cmdFlag = False
        for element in self._TUP_HUICOBUS_MSG_MATRIX:
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
    cls.func_data_send({'test':1})
    cls.client_publish_test({'srcNode':'HUICOBUS_MQTT_NODEID_TUPSVR', 'destNode':'HUICOBUS_MQTT_NODEID_TUPSVR', 'srcId':'HUICOBUS_MQTT_CLIENTID_TUPROUTER', 'destId':'HUICOBUS_MQTT_CLIENTID_TUPENTRY', 'topicId':'HUICOBUS_MQTT_TOPIC_UIP2TUP', 'cmdId':2689, 'cmdValue':123, 'hlContent':{'a':1, 'b':2}})














        
        
        
        
        