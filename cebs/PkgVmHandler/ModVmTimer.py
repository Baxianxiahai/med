'''
Created on 2018年12月10日

@author: Administrator
'''

import random
import time
from multiprocessing import Queue, Process
from PkgVmHandler import ModVmCfg
from PkgVmHandler import ModVmLayer


class tupTaskTimer(ModVmLayer.tupTaskTemplate):
    _STM_ACTIVE = 3

    def __init__(self):
        ModVmLayer.tupTaskTemplate.__init__(self, taskid=ModVmCfg.TUP_TASK_ID_TIMER, taskName="TASK_TIMER")
        ModVmLayer.TUP_GL_CFG.save_task_by_id(ModVmCfg.TUP_TASK_ID_TIMER, self)
        self.fsm_set(ModVmLayer.TUP_STM_NULL)
        #STM MATRIX
        self.add_stm_combine(ModVmLayer.TUP_STM_INIT, ModVmCfg.TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(ModVmLayer.TUP_STM_COMN, ModVmCfg.TUP_MSGID_RESTART, self.fsm_msg_restart_rcv_handler)
        self.add_stm_combine(ModVmLayer.TUP_STM_COMN, ModVmCfg.TUP_MSGID_TIME_OUT, self.fsm_msg_time_out_rcv_handler)
        self.fsm_set(ModVmLayer.TUP_STM_INIT)
        #print("State = ", self.fsm_get())
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


        
        
        
        
        
        
        