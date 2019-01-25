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
from PkgL3cebsHandler.ModCebsUiBasic import *


class tupTaskUiMeng(tupClassUiBasic):
    _STM_WORKING = 5    #从5开始属于任务私有部分

    def __init__(self, glPar):
        tupClassUiBasic.__init__(self, taskidUb=TUP_TASK_ID_UI_MENG, taskNameUb="TASK_UI_MENG", glParUb=glPar)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_MENG_UI_SWITCH, self.fsm_msg_ui_focus_rcv_handler)
        #业务态
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_MENG_MOTO_CMD_FB, self.fsm_msg_meng_cmd_fb_rcv_handler)
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()
        
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

    #清理各项操作：工程模式均为阻塞式工作模式，暂时不需要再去通知MENG任务模块 - 重载
    def func_ui_click_basic_close(self):
        print("I am func_ui_click_meng_close!")
        self.msg_send(TUP_MSGID_MENG_CLOSE_REQ, TUP_TASK_ID_MENG, "")
            









