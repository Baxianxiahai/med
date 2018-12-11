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


class tupTaskCtrlSchd(ModVmLayer.tupTaskTemplate):
    _STM_ACTIVE = 3

    def __init__(self):
        ModVmLayer.tupTaskTemplate.__init__(self, taskid=ModVmCfg.TUP_TASK_ID_CTRL_SCHD, taskName="TASK_CTRL_SCHD")
        #ModVmLayer.TUP_GL_CFG.save_task_by_id(ModVmCfg.TUP_TASK_ID_CTRL_SCHD, self)
        self.fsm_set(ModVmLayer.TUP_STM_NULL)
        #STM MATRIX
        self.add_stm_combine(ModVmLayer.TUP_STM_INIT, ModVmCfg.TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(ModVmLayer.TUP_STM_COMN, ModVmCfg.TUP_MSGID_RESTART, self.fsm_msg_restart_rcv_handler)
        self.add_stm_combine(ModVmLayer.TUP_STM_COMN, ModVmCfg.TUP_MSGID_TIME_OUT, self.fsm_msg_time_out_rcv_handler)
        self.fsm_set(ModVmLayer.TUP_STM_INIT)
        #START TASK
        self.task_run()

    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        time.sleep(0.5) #WAIT FOR OTHER TASK STARTUP

    def fsm_msg_restart_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        
    def fsm_msg_time_out_rcv_handler(self, msgContent):
        pass















