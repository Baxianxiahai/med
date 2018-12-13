'''
Created on 2018年12月10日

@author: Administrator
'''

import random
import time
from multiprocessing import Queue, Process
from PkgVmHandler.ModVmCfg import *
from PkgVmHandler.ModVmLayer import *


class tupTaskTimer(tupTaskTemplate):
    _STM_ACTIVE = 3

    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_TIMER, taskName="TASK_TIMER", glTabEntry=glPar)
        #ModVmLayer.TUP_GL_CFG.save_task_by_id(ModVmCfg.TUP_TASK_ID_TIMER, self)
        self.fsm_set(TUP_STM_NULL)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TIME_OUT, self.fsm_msg_time_out_rcv_handler)
        self.fsm_set(TUP_STM_INIT)
        
        #业务处理
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TIME_REQ, self.fsm_msg_time_req_rcv_handler)
        
        #START TASK
        self.task_run()

    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;

    def fsm_msg_restart_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        return TUP_SUCCESS;
        
    def fsm_msg_time_out_rcv_handler(self, msgContent):
        return TUP_SUCCESS;

    def fsm_msg_time_req_rcv_handler(self, msgContent):
        tid = int(msgContent['tid'])
        tType = int(msgContent['type'])
        cnt = int(msgContent['cnt'])
        if (tid <=0 ) or (tid >= self.glTab.TUP_TIMER_MAX):
            return TUP_FAILURE;
        if (tType != TUP_TIMER_ONE_TIME) and (tType != TUP_TIMER_PERIOD):
            return TUP_FAILURE;
        if (cnt < 0) and (cnt > 1000000):
            return TUP_FAILURE;
        #正常干活
        pass
        return TUP_SUCCESS;
    
        
        
        
        
        
        
        