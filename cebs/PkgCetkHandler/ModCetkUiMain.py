'''
Created on 2018年12月11日

@author: Administrator
'''

import random
import time
import sys
import json
import os
import re
import urllib
import http
import socket
from multiprocessing import Queue, Process
from PkgVmHandler.ModVmCfg import *
from PkgVmHandler.ModVmLayer import *
from PkgCebsHandler.ModCebsCom import *
from PkgCebsHandler.ModCebsCfg import *
from PkgVmHandler.ModVmConsole import *

from cebsTkL4Ui import *

class tupTaskUiMain(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3
    _STM_DEACT  = 4 #界面没激活
    
    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_UI_MAIN, taskName="TASK_UI_MAIN", glTabEntry=glPar)
        self.fsm_set(TUP_STM_NULL)
        self.fatherUiObj = ''   #父对象界面，双向通信
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TRACE, self.fsm_msg_trace_inc_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_MAIN_UI_SWITCH, self.fsm_msg_ui_focus_rcv_handler)
        #测试消息，后面可以去掉
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TEST, self.fsm_msg_print_test_inc_rcv_handler)
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()
    
    #延迟一秒，确保打印消息不丢失
    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        time.sleep(1)
        #第一次界面启动，肯定在MAIN界面这儿，所以需要给CTRL_SCHD模块一个启动信号
        self.msg_send(TUP_MSGID_CTRL_SCHD_SWITCH_ON, TUP_TASK_ID_CTRL_SCHD, "")
        self.msg_send(TUP_MSGID_MAIN_UI_SWITCH, TUP_TASK_ID_MOTO, "") 
        self.msg_send(TUP_MSGID_MAIN_UI_SWITCH, TUP_TASK_ID_VISION, "") 
        return TUP_SUCCESS;

    def fsm_msg_restart_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;

    def fsm_msg_trace_inc_rcv_handler(self, msgContent):
        self.funcDebugPrint2Qt(msgContent);
        return TUP_SUCCESS;

    def fsm_msg_ui_focus_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;
    
    def fsm_msg_print_test_inc_rcv_handler(self, msgContent):
        self.funcDebugPrint2Qt(msgContent);
        return TUP_SUCCESS;
    
    #将界面对象传递给本任务，以便将打印信息送到界面上
    def funcSaveFatherInst(self, instance):
        self.fatherUiObj = instance
    
    def funcDebugPrint2Qt(self, string):
        if (self.fatherUiObj == ''):
            print("MAIN_UI task lose 1 print message due to time sync.")
        else:
            self.fatherUiObj.cetk_debug_print(str(string))
    
    #主界面承接过来的执行函数-测试函数
    def funcPrintTestCalledByQt(self, string):
        self.funcDebugPrint2Qt(string);

        
    '''
    #主界面承接过来的执行函数
    '''
    def func_ui_click_cap_start_nor(self):
        print("I am func_ui_click_cap_start_nor!")
        self.msg_send(TUP_MSGID_CTRL_SCHD_CAPPIC_START, TUP_TASK_ID_CTRL_SCHD, "")

    def func_ui_click_cap_start_flu(self):
        print("I am func_ui_click_cap_start_flu!")
        self.msg_send(TUP_MSGID_CTRL_SCHD_CAPFLU_START, TUP_TASK_ID_CTRL_SCHD, "")

    def func_ui_click_cap_stop(self):
        print("I am func_ui_click_cap_stop!")
        self.msg_send(TUP_MSGID_CTRL_SCHD_CAPPIC_STOP, TUP_TASK_ID_CTRL_SCHD, "")
    
    def func_ui_click_move_zero(self):
        print("I am func_ui_click_move_zero!")
        self.msg_send(TUP_MSGID_CTRL_SCHD_MV_ZERO, TUP_TASK_ID_CTRL_SCHD, "")

    def func_ui_click_clf_start_nor(self):
        print("I am func_ui_click_clf_start_nor!")
        self.msg_send(TUP_MSGID_CTRL_SCHD_CFYFLU_START, TUP_TASK_ID_CTRL_SCHD, "")

    def func_ui_click_clf_start_flu(self):
        print("I am func_ui_click_clf_start_flu!")        
        self.msg_send(TUP_MSGID_CTRL_SCHD_CFYFLU_START, TUP_TASK_ID_CTRL_SCHD, "")
        
    def func_ui_click_clf_stop(self):
        print("I am func_ui_click_clf_stop!")        
        self.msg_send(TUP_MSGID_CTRL_SCHD_CFYPIC_STOP, TUP_TASK_ID_CTRL_SCHD, "")
    
    #切换界面
    def func_ui_click_calib_start(self):
        print("I am func_ui_click_calib_start!")
        self.msg_send(TUP_MSGID_CALIB_UI_SWITCH, TUP_TASK_ID_UI_CALIB, "")
        self.msg_send(TUP_MSGID_CALIB_UI_SWITCH, TUP_TASK_ID_MOTO, "")
        self.msg_send(TUP_MSGID_CALIB_UI_SWITCH, TUP_TASK_ID_VISION, "")
        self.msg_send(TUP_MSGID_CTRL_SCHD_SWITCH_OFF, TUP_TASK_ID_CTRL_SCHD, "")     
        #执行命令
        #发送停止CAP， 发送CFY停止
        #转移状态
        self.fsm_set(self._STM_DEACT)
    
    #切换界面
    def func_ui_click_gpar_start(self):
        print("I am func_ui_click_gpar_start!")
        self.msg_send(TUP_MSGID_GPAR_UI_SWITCH, TUP_TASK_ID_UI_GPAR, "")
        self.msg_send(TUP_MSGID_GPAR_UI_SWITCH, TUP_TASK_ID_VISION, "")
        self.msg_send(TUP_MSGID_CTRL_SCHD_SWITCH_OFF, TUP_TASK_ID_CTRL_SCHD, "")     
        #执行命令 
        #转移状态
        self.fsm_set(self._STM_DEACT)
    
    #TBD
    def func_ui_click_pilot_stop(self):
        print("I am func_ui_click_pilot_stop!")    
    
    #切换界面
    def func_ui_click_meng_start(self):
        print("I am func_ui_click_meng_start!")    
        self.msg_send(TUP_MSGID_MENG_UI_SWITCH, TUP_TASK_ID_UI_MENG, "") 
        self.msg_send(TUP_MSGID_MENG_UI_SWITCH, TUP_TASK_ID_MOTO, "") 
        self.msg_send(TUP_MSGID_CTRL_SCHD_SWITCH_OFF, TUP_TASK_ID_CTRL_SCHD, "")     
        #执行命令 
        #转移状态
        self.fsm_set(self._STM_DEACT)

    #切换界面
    def func_ui_click_main_start(self):
        print("I am func_ui_click_main_start!")
        self.msg_send(TUP_MSGID_MAIN_UI_SWITCH, TUP_TASK_ID_MOTO, "") 
        self.msg_send(TUP_MSGID_MAIN_UI_SWITCH, TUP_TASK_ID_VISION, "") 
        self.msg_send(TUP_MSGID_CTRL_SCHD_SWITCH_ON, TUP_TASK_ID_CTRL_SCHD, "")
        #执行命令 
        #转移状态
        self.fsm_set(self._STM_ACTIVE)



    





