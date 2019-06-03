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
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_HUICOBUS_L2FRAME_RCV, self.fsm_huicobus_l2frame_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_GPAR_GET_CFG_RESP, self.fsm_huicobus_gpar_get_cfg_resp_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_GPAR_SET_CFG_RESP, self.fsm_huicobus_gpar_set_cfg_resp_handler)
        
        
#         self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_HUICOBUS_GET_CFG_REQ, self.fsm_msg_dl_get_cfg_req_rcv_handler)
#         self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_HUICOBUS_GET_CFG_RESP, self.fsm_msg_ul_get_cfg_resp_rcv_handler)
#         self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_HUICOBUS_SET_CFG_REQ, self.fsm_msg_dl_set_cfg_req_rcv_handler)
#         self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_HUICOBUS_SET_CFG_RESP, self.fsm_msg_ul_set_cfg_resp_rcv_handler)

        
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()
 
    '''
    #
    #SERVICE PROCESSING
    #
    '''
    def fsm_huicobus_l2frame_rcv_handler(self, msgContent):
        cmdId = msgContent['cmdId']
        mbuf={}
        mbuf['cmdvalue'] = msgContent['cmdValue']
        mbuf['hlContent'] = msgContent['hlContent']
        if (cmdId == TUP_HHD_CMDID_SYS_GET_CONFIG_REQ):
            self.msg_send(TUP_MSGID_GPAR_GET_CFG_REQ, TUP_TASK_ID_GPAR, mbuf)
        elif (cmdId == TUP_HHD_CMDID_SYS_SET_CONFIG_REQ):
            self.msg_send(TUP_MSGID_GPAR_SET_CFG_REQ, TUP_TASK_ID_GPAR, mbuf)
        return TUP_SUCCESS

    def fsm_huicobus_gpar_get_cfg_resp_rcv_handler(self, msgContent):
        mbuf={}
        mbuf['hlContent'] = msgContent
        ret = self.func_huicobus_msg_snd(TUP_HHD_CMDID_SYS_GET_CONFIG_RESP, msgContent['cmdValue'], mbuf)
        return ret

    def fsm_huicobus_gpar_set_cfg_resp_handler(self, msgContent):
        mbuf={}
        mbuf['hlContent'] = msgContent
        ret = self.func_huicobus_msg_snd(TUP_HHD_CMDID_SYS_SET_CONFIG_RESP, msgContent['cmdValue'], mbuf)
        return ret


















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














    
    