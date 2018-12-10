'''
Created on 2018年12月8日

@author: Administrator
'''

import random
import time
from multiprocessing import Queue, Process
from PkgVmHandler import ModVmCfg
from PkgVmHandler import ModVmLayer
from PkgCebsHandler import ModCebsCom
from PkgCebsHandler import ModCebsCfg


class tupTaskVision(ModVmLayer.tupTaskTemplate):
    _STM_ACTIVE = 3
    #主界面，干活拍照
    _STM_MAIN_UI_ACT = 4
    #校准模式下图像直接读取
    _STM_CALIB_UI_ACT = 5

    def __init__(self):
        ModVmLayer.tupTaskTemplate.__init__(self, taskid=ModVmCfg.TUP_TASK_ID_VISION, taskName="TASK_VISION")
        ModVmLayer.TUP_GL_CFG.save_task_by_id(ModVmCfg.TUP_TASK_ID_TIMER, self)
        self.fsm_set(ModVmLayer.TUP_STM_NULL)
        #STM MATRIX
        self.add_stm_combine(ModVmLayer.TUP_STM_INIT, ModVmCfg.TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(ModVmLayer.TUP_STM_COMN, ModVmCfg.TUP_MSGID_RESTART, self.fsm_msg_restart_rcv_handler)
        self.add_stm_combine(ModVmLayer.TUP_STM_COMN, ModVmCfg.TUP_MSGID_TIME_OUT, self.fsm_msg_time_out_rcv_handler)
        #通知界面切换
        self.add_stm_combine(ModVmLayer.TUP_STM_COMN, ModVmCfg.TUP_MSGID_MAIN_UI_SWITCH, self.fsm_msg_main_ui_switch_rcv_handler)
        self.add_stm_combine(ModVmLayer.TUP_STM_COMN, ModVmCfg.TUP_MSGID_CALIB_UI_SWITCH, self.fsm_msg_calib_ui_switch_rcv_handler)
        #切换状态机
        self.fsm_set(ModVmLayer.TUP_STM_INIT)
        #START TASK
        self.task_run()

    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        time.sleep(0.5) #WAIT FOR OTHER TASK STARTUP

    def fsm_msg_restart_rcv_handler(self, msgContent):
        time.sleep(1)
        self.fsm_set(self._STM_ACTIVE)
        
    def fsm_msg_time_out_rcv_handler(self, msgContent):
        time.sleep(1)

    def fsm_msg_main_ui_switch_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_MAIN_UI_ACT)

    def fsm_msg_calib_ui_switch_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_CALIB_UI_ACT)

    def funcVisionLogTrace(self, myString):
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
        else:
            self.tup_err_print("Not in right state.")








