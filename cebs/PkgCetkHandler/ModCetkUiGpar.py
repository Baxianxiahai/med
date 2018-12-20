'''
Created on 2018年12月11日

@author: Administrator
'''

import random
import time
from multiprocessing import Queue, Process
from PkgVmHandler.ModVmCfg import *
from PkgVmHandler.ModVmLayer import *
from PkgCebsHandler.ModCebsCom import *
from PkgCebsHandler.ModCebsCfg import *
from PkgVmHandler.ModVmConsole import *


class tupTaskUiGpar(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3
    _STM_DEACT  = 4 #界面没激活

    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_UI_GPAR, taskName="TASK_UI_GPAR", glTabEntry=glPar)
        self.fsm_set(TUP_STM_NULL)
        self.fatherUiObj = ''   #父对象界面，双向通信
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TRACE, self.fsm_msg_trace_inc_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_GPAR_UI_SWITCH, self.fsm_msg_ui_focus_rcv_handler)
        
        #业务处理函数
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_GPAR_PIC_TRAIN_RESP, self.fsm_msg_pic_train_resp_rcv_handler)
        
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()

    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_DEACT)
        return TUP_SUCCESS;

    def fsm_msg_restart_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_DEACT)
        return TUP_SUCCESS;
    
    def fsm_msg_trace_inc_rcv_handler(self, msgContent):
        self.funcDebugPrint2Qt(msgContent);
        return TUP_SUCCESS;

    def fsm_msg_pic_train_resp_rcv_handler(self, msgContent):
        if (msgContent['res'] < 0):
            self.funcDebugPrint2Qt("Train picture failure!");
        else:
            self.fatherUiObj.gpar_callback_train_resp(msgContent['fileName'])
        return TUP_SUCCESS;

    #界面切换进来
    def fsm_msg_ui_focus_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;
    
    #将界面对象传递给本任务，以便将打印信息送到界面上
    def funcSaveFatherInst(self, instance):
        self.fatherUiObj = instance
    
    #将界面参数传递给业务模块
    def funcGparInitBascPar(self, orgWidth, orgHeight, cfyWidth, cfyHeight):
        mbuf = {}
        mbuf['orgWidth'] = orgWidth
        mbuf['orgHeight'] = orgHeight
        mbuf['cfyWidth'] = cfyWidth
        mbuf['cfyHeight'] = cfyHeight
        self.msg_send(TUP_MSGID_GPAR_INIT_INF, TUP_TASK_ID_GPAR, mbuf)
    
    def funcDebugPrint2Qt(self, string):
        if (self.fatherUiObj == ''):
            print("GPAR_UI task lose 1 print message due to time sync.")
        else:
            self.fatherUiObj.cetk_debug_print(str(string))
            
    #主界面承接过来的执行函数   
    def func_ui_click_pic_train(self, fileName):
        print("I am func_ui_click_pic_train!")
        #LC:before click train you need to send message to refresh train pars
        mbuf={}
        self.msg_send(TUP_MSGID_GPAR_REFRESH_PAR, TUP_TASK_ID_VISION, mbuf) 
        mbuf={}
        mbuf['fileName'] = fileName 
        self.msg_send(TUP_MSGID_GPAR_PIC_TRAIN_REQ, TUP_TASK_ID_GPAR, mbuf)
    
    def func_ui_click_gpar_refresh_par(self):
        print("I am func_ui_click_gpar_refresh_par!")
        mbuf={}
        self.msg_send(TUP_MSGID_GPAR_REFRESH_PAR, TUP_TASK_ID_VISION, mbuf)        
    
    #清理各项操作
    def func_ui_click_gpar_close(self):
        print("I am func_ui_click_gpar_close!")
        self.msg_send(TUP_MSGID_GPAR_CLOSE_REQ, TUP_TASK_ID_GPAR, "")
        
    #界面切走
    def func_ui_click_gpar_switch_to_main(self):
        print("I am func_ui_click_gpar_switch_to_main!")
        self.fsm_set(self._STM_DEACT)           
        
        
        
        
        
        
        
        

















