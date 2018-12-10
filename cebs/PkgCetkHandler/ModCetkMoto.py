'''
Created on 2018年12月8日

@author: Administrator
'''

import random
import sys
import time
import json
import os
import re
import urllib
import http
import socket
import serial
import serial.tools.list_ports
import struct

from multiprocessing import Queue, Process
from PkgVmHandler import ModVmCfg
from PkgVmHandler import ModVmLayer
from PkgCebsHandler import ModCebsCom
from PkgCebsHandler import ModCebsCfg


#主任务入口
class tupTaskMoto(ModVmLayer.tupTaskTemplate):
    _STM_ACTIVE = 3
    #主界面，干活拍照
    _STM_MAIN_UI_ACT = 4
    #校准界面，校准移动马达
    _STM_CALIB_UI_ACT = 5
    #工程模式，操控马达配置
    _STM_MENG_UI_ACT = 6

    def __init__(self):
        ModVmLayer.tupTaskTemplate.__init__(self, taskid=ModVmCfg.TUP_TASK_ID_MOTO, taskName="TASK_MOTO")
        ModVmLayer.TUP_GL_CFG.save_task_by_id(ModVmCfg.TUP_TASK_ID_TIMER, self)
        self.fsm_set(ModVmLayer.TUP_STM_NULL)
        #STM MATRIX
        self.add_stm_combine(ModVmLayer.TUP_STM_INIT, ModVmCfg.TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(ModVmLayer.TUP_STM_COMN, ModVmCfg.TUP_MSGID_RESTART, self.fsm_msg_restart_rcv_handler)
        self.add_stm_combine(ModVmLayer.TUP_STM_COMN, ModVmCfg.TUP_MSGID_TIME_OUT, self.fsm_msg_time_out_rcv_handler)
        #通知界面切换
        self.add_stm_combine(ModVmLayer.TUP_STM_COMN, ModVmCfg.TUP_MSGID_MAIN_UI_SWITCH, self.fsm_msg_main_ui_switch_rcv_handler)
        self.add_stm_combine(ModVmLayer.TUP_STM_COMN, ModVmCfg.TUP_MSGID_CALIB_UI_SWITCH, self.fsm_msg_calib_ui_switch_rcv_handler)
        self.add_stm_combine(ModVmLayer.TUP_STM_COMN, ModVmCfg.TUP_MSGID_MENG_UI_SWITCH, self.fsm_msg_meng_ui_switch_rcv_handler)
        #切换状态机
        self.fsm_set(ModVmLayer.TUP_STM_INIT)
        #START TASK
        self.task_run()

    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        time.sleep(0.5) #WAIT FOR OTHER TASK STARTUP
        ModCebsCom.GLPLT_PAR_OFC.med_init_plate_parameter()
        self.instL1ConfigOpr = ModCebsCfg.clsL1_ConfigOpr()

    def fsm_msg_restart_rcv_handler(self, msgContent):
        time.sleep(1)
        self.fsm_set(self._STM_ACTIVE)
        
    def fsm_msg_time_out_rcv_handler(self, msgContent):
        time.sleep(1)

    def fsm_msg_main_ui_switch_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_MAIN_UI_ACT)

    def fsm_msg_calib_ui_switch_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_CALIB_UI_ACT)

    def fsm_msg_meng_ui_switch_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_MENG_UI_ACT)
        
    def funcMotoLogTrace(self, myString):
        msgSnd = {}
        msgSnd['mid'] = ModVmCfg.TUP_MSGID_TRACE
        msgSnd['src'] = self.taskId
        msgSnd['content'] = myString
        self.fsm_set(self._STM_ACTIVE)
        if (self.state == self._STM_MAIN_UI_ACT):
            msgSnd['dst'] = ModVmCfg.TUP_TASK_ID_UI_MAIN
            self.msg_send_out(ModVmCfg.TUP_TASK_ID_UI_MAIN, msgSnd)
        elif (self.state == self._STM_CALIB_UI_ACT):
            msgSnd['dst'] = ModVmCfg.TUP_TASK_ID_UI_CALIB
            self.msg_send_out(ModVmCfg.TUP_TASK_ID_UI_CALIB, msgSnd)
        elif (self.state == self._STM_MENG_UI_ACT):
            msgSnd['dst'] = ModVmCfg.TUP_TASK_ID_UI_MENG
            self.msg_send_out(ModVmCfg.TUP_TASK_ID_UI_MENG, msgSnd)
        else:
            self.tup_err_print("Not in right state.")
        return
    
'''
业务部分
'''






















