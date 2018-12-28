'''
Created on 2018年12月11日

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


class tupTaskUiMeng(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3
    _STM_DEACT  = 4 #界面没激活

    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_UI_MENG, taskName="TASK_UI_MENG", glTabEntry=glPar)
        self.fsm_set(TUP_STM_NULL)
        self.fatherUiObj = ''   #父对象界面，双向通信
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_com_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_EXIT, self.fsm_com_msg_exit_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TEST, self.fsm_com_msg_test_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TRACE, self.fsm_msg_trace_inc_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_MENG_UI_SWITCH, self.fsm_msg_ui_focus_rcv_handler)
        #业务态
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_MENG_MOTO_CMD_FB, self.fsm_msg_meng_cmd_fb_rcv_handler)
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()

    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_DEACT)
        return TUP_SUCCESS;

    def fsm_msg_trace_inc_rcv_handler(self, msgContent):
        self.funcDebugPrint2Qt(msgContent);
        return TUP_SUCCESS;
        
    #业务状态处理过程
    #jsonDic = json.loads(msgContent)
    def fsm_msg_meng_cmd_fb_rcv_handler(self, msgContent):
        if (self.fatherUiObj == ''):
            print("MENG_UI task lose 1 print message due to time sync.")
        else:      
            #self.funcDebugPrint2Qt(msgContent)
            self.fatherUiObj.meng_callback_cmd_exec_fb(msgContent['res'])
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
            print("MENG_UI task lose 1 print message due to time sync.")
        else:
            self.fatherUiObj.cetk_debug_print(str(string))
            
    #主界面承接过来的执行函数
    def func_ui_click_send_command(self, cmdid, par1, par2, par3, par4):
        print("I am func_ui_click_send_command!")
        mbuf = {}
        mbuf['cmdid'] = int(cmdid)
        mbuf['par1'] = int(par1)
        mbuf['par2'] = int(par2)
        mbuf['par3'] = int(par3)
        mbuf['par4'] = int(par4)
        self.msg_send(TUP_MSGID_MENG_MOTO_COMMAND, TUP_TASK_ID_MENG, mbuf)

    #清理各项操作：工程模式均为阻塞式工作模式，暂时不需要再去通知MENG任务模块
    def func_ui_click_meng_close(self):
        print("I am func_ui_click_meng_close!")
        self.msg_send(TUP_MSGID_MENG_CLOSE_REQ, TUP_TASK_ID_MENG, "")
            
    #界面切走
    def func_ui_click_meng_switch_to_main(self):
        print("I am func_ui_click_meng_switch_to_main!")
        self.fsm_set(self._STM_DEACT)          









