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
from PkgVmHandler.ModVmTimer import *


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
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TIME_OUT, self.fsm_msg_time_out_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TRACE, self.fsm_msg_trace_inc_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_GPAR_UI_SWITCH, self.fsm_msg_ui_focus_rcv_handler)
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()

    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_DEACT)
        return TUP_SUCCESS;

    def fsm_msg_restart_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_DEACT)
        return TUP_SUCCESS;
        
    def fsm_msg_time_out_rcv_handler(self, msgContent):
        return TUP_SUCCESS;

    def fsm_msg_trace_inc_rcv_handler(self, msgContent):
        self.funcDebugPrint2Qt(msgContent);
        return TUP_SUCCESS;

    #界面切换进来
    def fsm_msg_ui_focus_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;
    
    #将界面对象传递给本任务，以便将打印信息送到界面上
    def funcSaveFatherInst(self, instance):
        self.fatherUiObj = instance
    
    def funcDebugPrint2Qt(self, string):
        if (self.fatherUiObj == ''):
            print("GPAR_UI task lose 1 print message due to time sync.")
        else:
            self.fatherUiObj.cetk_debug_print(str(string))
            
    #主界面承接过来的执行函数
    def func_ui_click_pic_file_load(self, fn):
        print("I am func_ui_click_pic_file_load!")
    
    def func_ui_click_pic_train(self):
        print("I am func_ui_click_pic_train!")
    
    #清理各项操作
    def func_ui_click_gpar_close(self):
        print("I am func_ui_click_gpar_close!")
        
    #界面切走
    def func_ui_click_gpar_switch_to_main(self):
        print("I am func_ui_click_gpar_switch_to_main!")
        self.fsm_set(self._STM_DEACT)           
        
        
        
        
        
        
        
        
        

















