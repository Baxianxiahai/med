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
from PkgVmHandler.ModVmTimer import *

from cebsTkL4Ui import *

class tupTaskUiMain(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3
    
    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_UI_MAIN, taskName="TASK_UI_MAIN", glTabEntry=glPar)
        self.fsm_set(TUP_STM_NULL)
        #self.qstSubTask = tupTaskUiMainThread()
        self.instUiTk = ''
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TIME_OUT, self.fsm_msg_time_out_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TRACE, self.fsm_msg_trace_inc_rcv_handler)
        #测试消息，后面可以去掉
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TEST, self.fsm_msg_print_test_inc_rcv_handler)
        self.fsm_set(TUP_STM_INIT)
        #START TASK
        self.task_run()
    
    #延迟一秒，确保打印消息不丢失
    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        time.sleep(1)
        return TUP_SUCCESS;

    def fsm_msg_restart_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;
        
    def fsm_msg_time_out_rcv_handler(self, msgContent):
        return TUP_SUCCESS;

    def fsm_msg_trace_inc_rcv_handler(self, msgContent):
        self.funcDebugPrint2Qt(msgContent);
        return TUP_SUCCESS;
    
    def fsm_msg_print_test_inc_rcv_handler(self, msgContent):
        self.funcDebugPrint2Qt(msgContent);
        return TUP_SUCCESS;
    
    #将界面对象传递给本任务，以便将打印信息送到界面上
    def funcSaveUiInstance(self, instance):
        self.instUiTk = instance
    
    def funcDebugPrint2Qt(self, string):
        if (self.instUiTk == ''):
            print("MAIN_UI task lose 1 print message due to time sync.")
        else:
            self.instUiTk.med_debug_print(string)
    
    #主界面承接过来的执行函数-测试函数
    def funcPrintTestCalledByQt(self, string):
        self.funcDebugPrint2Qt(string);
        #self.msg_send(TUP_MSGID_TEST, TUP_TASK_ID_UI_MAIN, TUP_TASK_ID_UI_MAIN, string)


        
    '''
    #主界面承接过来的执行函数
    '''
    def func_ui_click_cap_start_nor(self):
        print("I am func_ui_click_cap_start_nor!")

    def func_ui_click_cap_start_flu(self):
        print("I am func_ui_click_cap_start_flu!")

    def func_ui_click_cap_stop(self):
        print("I am func_ui_click_cap_stop!")
    
    def func_ui_click_move_zero(self):
        print("I am func_ui_click_move_zero!")

    def func_ui_click_clf_start_nor(self):
        print("I am func_ui_click_clf_start_nor!")

    def func_ui_click_clf_start_flu(self):
        print("I am func_ui_click_clf_start_flu!")        
        
    def func_ui_click_clf_stop(self):
        print("I am func_ui_click_clf_stop!")        
    
    #切换界面
    def func_ui_click_calib_start(self):
        print("I am func_ui_click_calib_start!")
        #切换界面
        #执行命令 
    
    #切换界面
    def func_ui_click_gpar_start(self):
        print("I am func_ui_click_gpar_start!")    
    
    #切换界面
    def func_ui_click_meng_start(self):
        print("I am func_ui_click_meng_start!")    

    #切换界面
    def func_ui_click_main_start(self):
        print("I am func_ui_click_main_start!")    



    





