'''
Created on 2019年2月19日

@author: Administrator
'''
from PkgL2svrHandler.ModHuicobus import *
from PkgL3cebsHandler.ModCebsCom import *
from PkgL3cebsHandler.ModCebsCfg import *

class TupClsCebsHuicobusItf(TupClsHuicobusBasic, clsL1_ConfigOpr):
    '''
    classdocs
    '''
    _STM_WORKING = 5    #从5开始属于任务私有部分

    def __init__(self, glPar):
        '''
        Constructor
        '''
        TupClsHuicobusBasic.__init__(self, taskidUb=TUP_TASK_ID_HUICOBUS, taskNameUb="TASK_HUICOBUS", glParUb=glPar)
        #STM MATRIX
        #业务处理部分
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_HUICOBUS_GET_CFG_REQ, self.fsm_msg_dl_get_cfg_req_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_HUICOBUS_GET_CFG_RESP, self.fsm_msg_ul_get_cfg_resp_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_HUICOBUS_SET_CFG_REQ, self.fsm_msg_dl_set_cfg_req_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_HUICOBUS_SET_CFG_RESP, self.fsm_msg_ul_set_cfg_resp_rcv_handler)


#         self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_HUICOBUS_CTRL_REQ, self.fsm_msg_ctrl_req_rcv_handler)
#         self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_HUICOBUS_CTRL_CONFIRM, self.fsm_msg_ctrl_confirm_rcv_handler)
#         self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_HUICOBUS_MOTO_CONFIRM, self.fsm_msg_moto_confirm_rcv_handler)
#         self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_HUICOBUS_CAM_CONFIRM, self.fsm_msg_cam_confirm_rcv_handler)
#         self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_HUICOBUS_CALIB_CONFIRM, self.fsm_msg_calib_confirm_rcv_handler)
#         self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_HUICOBUS_TEST_CMD_CONFIRM, self.fsm_msg_test_cmd_confirm_rcv_handler)
#         self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_HUICOBUS_CFY_CONFIRM, self.fsm_msg_cfy_confirm_rcv_handler)
#         self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_HUICOBUS_NOTIFY, self.fsm_msg_notify_rcv_handler)
        
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()
 
    '''
    #
    #SERVICE PROCESSING
    #
    '''
    def fsm_msg_dl_get_cfg_req_rcv_handler(self, msgContent):
        mbuf={}
        mbuf['cmdvalue'] = msgContent['cmdValue']
        temp = msgContent['hlContent']
        #未来待完善参数
        for element in temp:
            pass
        self.msg_send(TUP_MSGID_HUICOBUS_GET_CFG_REQ, TUP_TASK_ID_GPAR, mbuf)
        return TUP_SUCCESS

    def fsm_msg_ul_get_cfg_resp_rcv_handler(self, msgContent):
        mbuf={}
        mbuf['hlContent'] = msgContent
        return self.func_huicobus_msg_snd(TUP_HHD_CMDID_SYS_GET_CONFIG_RESP, msgContent['cmdValue'], mbuf)

    def fsm_msg_dl_set_cfg_req_rcv_handler(self, msgContent):
        return TUP_SUCCESS        
    
    #msgContent 应该包含cmdValue, hlContent
    def fsm_msg_ul_set_cfg_resp_rcv_handler(self, msgContent):
        return self.func_huicobus_msg_snd(TUP_HHD_CMDID_SYS_SET_CONFIG_RESP, msgContent['cmdValue'], msgContent['hlContent'])

        
#     def fsm_msg_ctrl_req_rcv_handler(self, msgContent):
#         jsonInput = {}
#         jsonInput['srcNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
#         jsonInput['destNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
#         jsonInput['srcId'] = 'HUICOBUS_MQTT_CLIENTID_TUPENTRY'
#         jsonInput['destId'] = 'HUICOBUS_MQTT_CLIENTID_TUPROUTER'
#         jsonInput['topicId'] = 'HUICOBUS_MQTT_TOPIC_TUP2UIR'
#         jsonInput['cmdId'] = 0
#         for element in self._TUP_HUIJSON_MSG_MATRIX:
#             if (element['topic'] == jsonInput['topicId']) and (element['cmdName'] == 'HUICOBUS_CMDID_cui_tup2uir_ctrl_req'):
#                 jsonInput['cmdId'] = element['cmdId']
#         jsonInput['cmdValue'] = msgContent['cmdValue']
#         jsonInput['hlContent'] = msgContent['hlContent']
#         self.func_data_send(jsonInput)
#         return TUP_SUCCESS
# 
#     def fsm_msg_ctrl_confirm_rcv_handler(self, msgContent):
#         jsonInput = {}
#         jsonInput['srcNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
#         jsonInput['destNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
#         jsonInput['srcId'] = 'HUICOBUS_MQTT_CLIENTID_TUPENTRY'
#         jsonInput['destId'] = 'HUICOBUS_MQTT_CLIENTID_TUPROUTER'
#         jsonInput['topicId'] = 'HUICOBUS_MQTT_TOPIC_TUP2UIR'
#         jsonInput['cmdId'] = 0
#         for element in self._TUP_HUIJSON_MSG_MATRIX:
#             if (element['topic'] == jsonInput['topicId']) and (element['cmdName'] == 'HUICOBUS_CMDID_cui_tup2uir_ctrl_confirm'):
#                 jsonInput['cmdId'] = element['cmdId']
#         jsonInput['cmdValue'] = msgContent['cmdValue']
#         jsonInput['hlContent'] = msgContent['hlContent']
#         self.func_data_send(jsonInput)
#         return TUP_SUCCESS
#     
#     def fsm_msg_moto_confirm_rcv_handler(self, msgContent):
#         jsonInput = {}
#         jsonInput['srcNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
#         jsonInput['destNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
#         jsonInput['srcId'] = 'HUICOBUS_MQTT_CLIENTID_TUPENTRY'
#         jsonInput['destId'] = 'HUICOBUS_MQTT_CLIENTID_TUPROUTER'
#         jsonInput['topicId'] = 'HUICOBUS_MQTT_TOPIC_TUP2UIR'
#         jsonInput['cmdId'] = 0
#         for element in self._TUP_HUIJSON_MSG_MATRIX:
#             if (element['topic'] == jsonInput['topicId']) and (element['cmdName'] == 'HUICOBUS_CMDID_cui_tup2uir_moto_confirm'):
#                 jsonInput['cmdId'] = element['cmdId']
#         jsonInput['cmdValue'] = msgContent['cmdValue']
#         jsonInput['hlContent'] = msgContent['hlContent']
#         self.func_data_send(jsonInput)
#         return TUP_SUCCESS    
#     
#     def fsm_msg_cam_confirm_rcv_handler(self, msgContent):
#         jsonInput = {}
#         jsonInput['srcNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
#         jsonInput['destNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
#         jsonInput['srcId'] = 'HUICOBUS_MQTT_CLIENTID_TUPENTRY'
#         jsonInput['destId'] = 'HUICOBUS_MQTT_CLIENTID_TUPROUTER'
#         jsonInput['topicId'] = 'HUICOBUS_MQTT_TOPIC_TUP2UIR'
#         jsonInput['cmdId'] = 0
#         for element in self._TUP_HUIJSON_MSG_MATRIX:
#             if (element['topic'] == jsonInput['topicId']) and (element['cmdName'] == 'HUICOBUS_CMDID_cui_tup2uir_cam_confirm'):
#                 jsonInput['cmdId'] = element['cmdId']
#         jsonInput['cmdValue'] = msgContent['cmdValue']
#         jsonInput['hlContent'] = msgContent['hlContent']
#         self.func_data_send(jsonInput)
#         return TUP_SUCCESS    
#     
#     def fsm_msg_calib_confirm_rcv_handler(self, msgContent):
#         jsonInput = {}
#         jsonInput['srcNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
#         jsonInput['destNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
#         jsonInput['srcId'] = 'HUICOBUS_MQTT_CLIENTID_TUPENTRY'
#         jsonInput['destId'] = 'HUICOBUS_MQTT_CLIENTID_TUPROUTER'
#         jsonInput['topicId'] = 'HUICOBUS_MQTT_TOPIC_TUP2UIR'
#         jsonInput['cmdId'] = 0
#         for element in self._TUP_HUIJSON_MSG_MATRIX:
#             if (element['topic'] == jsonInput['topicId']) and (element['cmdName'] == 'HUICOBUS_CMDID_cui_tup2uir_calib_confirm'):
#                 jsonInput['cmdId'] = element['cmdId']
#         jsonInput['cmdValue'] = msgContent['cmdValue']
#         jsonInput['hlContent'] = msgContent['hlContent']
#         self.func_data_send(jsonInput)
#         return TUP_SUCCESS    
#     
#     def fsm_msg_test_cmd_confirm_rcv_handler(self, msgContent):
#         jsonInput = {}
#         jsonInput['srcNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
#         jsonInput['destNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
#         jsonInput['srcId'] = 'HUICOBUS_MQTT_CLIENTID_TUPENTRY'
#         jsonInput['destId'] = 'HUICOBUS_MQTT_CLIENTID_TUPROUTER'
#         jsonInput['topicId'] = 'HUICOBUS_MQTT_TOPIC_TUP2UIR'
#         jsonInput['cmdId'] = 0
#         for element in self._TUP_HUIJSON_MSG_MATRIX:
#             if (element['topic'] == jsonInput['topicId']) and (element['cmdName'] == 'HUICOBUS_CMDID_cui_tup2uir_test_cmd_confirm'):
#                 jsonInput['cmdId'] = element['cmdId']
#         jsonInput['cmdValue'] = msgContent['cmdValue']
#         jsonInput['hlContent'] = msgContent['hlContent']
#         self.func_data_send(jsonInput)
#         return TUP_SUCCESS
# 
#     def fsm_msg_cfy_confirm_rcv_handler(self, msgContent):
#         jsonInput = {}
#         jsonInput['srcNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
#         jsonInput['destNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
#         jsonInput['srcId'] = 'HUICOBUS_MQTT_CLIENTID_TUPENTRY'
#         jsonInput['destId'] = 'HUICOBUS_MQTT_CLIENTID_TUPROUTER'
#         jsonInput['topicId'] = 'HUICOBUS_MQTT_TOPIC_TUP2UIR'
#         jsonInput['cmdId'] = 0
#         for element in self._TUP_HUIJSON_MSG_MATRIX:
#             if (element['topic'] == jsonInput['topicId']) and (element['cmdName'] == 'HUICOBUS_CMDID_cui_tup2uir_cfy_confirm'):
#                 jsonInput['cmdId'] = element['cmdId']
#         jsonInput['cmdValue'] = msgContent['cmdValue']
#         jsonInput['hlContent'] = msgContent['hlContent']
#         self.func_data_send(jsonInput)
#         return TUP_SUCCESS
# 
#     def fsm_msg_notify_rcv_handler(self, msgContent):
#         jsonInput = {}
#         jsonInput['srcNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
#         jsonInput['destNode'] = 'HUICOBUS_MQTT_NODEID_TUPSVR'
#         jsonInput['srcId'] = 'HUICOBUS_MQTT_CLIENTID_TUPENTRY'
#         jsonInput['destId'] = 'HUICOBUS_MQTT_CLIENTID_TUPROUTER'
#         jsonInput['topicId'] = 'HUICOBUS_MQTT_TOPIC_TUP2UIR'
#         jsonInput['cmdId'] = 0
#         for element in self._TUP_HUIJSON_MSG_MATRIX:
#             if (element['topic'] == jsonInput['topicId']) and (element['cmdName'] == 'HUICOBUS_CMDID_cui_tup2uir_notify'):
#                 jsonInput['cmdId'] = element['cmdId']
#         jsonInput['cmdValue'] = msgContent['cmdValue']
#         jsonInput['hlContent'] = msgContent['hlContent']
#         self.func_data_send(jsonInput)
#         return TUP_SUCCESS


if __name__ == '__main__':
    #创建并初始化
    TUP_GL_CFG = tupGlbCfg()
    initMsg = {}
    initMsg['mid'] = TUP_MSGID_INIT
    initMsg['src'] = TUP_TASK_ID_TUPCONSL
    initMsg['content'] = ""
    cls = TupClsCebsHuicobusItf(TUP_GL_CFG);
    initMsg['dst'] = TUP_TASK_ID_HUICOBUS
    cls.msg_send_in(initMsg)
    cls.tup_dbg_print("Create HUICOBUS task success!")
    #注册上层应用模块
#     initMsg['mid'] = TUP_MSGID_HUICOBUS_REG_UP_USER
#     mbuf = {}
#     mbuf['userTaskId'] = TUP_TASK_ID_UI_GPAR
#     initMsg['content'] = mbuf
#     cls.msg_send_in(initMsg)
#     cls.func_data_send({'test':1})
#     time.sleep(1)
#     cls.client_test({'srcNode':'HUICOBUS_MQTT_NODEID_TUPSVR', \
#                 'destNode':'HUICOBUS_MQTT_NODEID_TUPSVR', \
#                 'srcId':'HUICOBUS_MQTT_CLIENTID_TUPROUTER', \
#                 'destId':'HUICOBUS_MQTT_CLIENTID_TUPENTRY', \
#                 'topicId':'HUICOBUS_MQTT_TOPIC_UIR2TUP', \
#                 'cmdId':2689, \
#                 'cmdValue':123, \
#                 'hlContent':{'a':1, 'b':2}\
#                 })














    
    