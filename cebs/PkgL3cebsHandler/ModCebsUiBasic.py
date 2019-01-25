'''
Created on 2019年1月25日

@author: Administrator
'''

####!/usr/bin/python3.6
#### -*- coding: UTF-8 -*-

import random
import time
import json
from multiprocessing import Queue, Process
from PkgL1vmHandler.ModVmCfg import *
from PkgL1vmHandler.ModVmLayer import *
from PkgL3cebsHandler.ModCebsCom import *
from PkgL3cebsHandler.ModCebsCfg import *
from PkgL1vmHandler.ModVmConsole import *


class tupClassUiBasic(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3
    _STM_DEACT  = 4 #界面没激活
    
    #全局变量表

    def __init__(self, taskidUb, taskNameUb, glParUb):
        tupTaskTemplate.__init__(self, taskid=taskidUb, taskName=taskNameUb, glTabEntry=glParUb)
        #super(tupClassUiBasic, self).__init__(self, taskidUb, taskNameUb, glParUb)
        self.fsm_set(TUP_STM_NULL)
        self.fatherUiObj = ''   #父对象界面，双向通信
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_com_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_EXIT, self.fsm_com_msg_exit_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TEST, self.fsm_com_msg_test_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TRACE, self.fsm_msg_trace_inc_rcv_handler)
    
    #核心处理函数，初始化
    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_DEACT)
        return TUP_SUCCESS;

    #核心处理函数，打印消息
    def fsm_msg_trace_inc_rcv_handler(self, msgContent):
        self.funcDebugPrint2Qt(msgContent);
        return TUP_SUCCESS;
        
    #将界面对象传递给本任务，以便将打印信息送到界面上
    def funcSaveFatherInst(self, instance):
        self.fatherUiObj = instance
    
    #标准打印函数
    def funcDebugPrint2Qt(self, string):
        if (self.fatherUiObj == ''):
            print("Task [", self.taskName, "] task lose 1 print message due to time sync.")
        else:
            self.fatherUiObj.cetk_debug_print(str(string))

    #界面切换进来
    def fsm_msg_ui_focus_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;
    
    #界面切走 - 模板
    def func_ui_click_basic_switch_to_main(self):
        print("I am func_ui_click_basic_switch_to_main!")
        self.fsm_set(self._STM_DEACT)       

    #清理各项操作 - 模板
    def func_ui_click_basic_close(self):
        print("I am func_ui_click_basic_close!")
  








        

