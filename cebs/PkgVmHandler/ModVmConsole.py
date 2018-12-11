'''
Created on 2018年12月10日

@author: Administrator
'''
import random
import time
from multiprocessing import Queue, Process
from PkgVmHandler.ModVmCfg import *
from PkgVmHandler.ModVmLayer import *


class tupTaskVmConsl(tupTaskTemplate):
    _STM_ACTIVE = 3
    _STM_RUN = 4
    _STM_CLOSE = 5
    _STM_MAX = 6

    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_VMCONSL, taskName="TASK_VM", glTabEntry=glPar)
        #ModVmLayer.TUP_GL_CFG.save_task_by_id(ModVmCfg.TUP_TASK_ID_VMCONSL, self)
        self.fsm_set(TUP_STM_NULL)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TIME_OUT, self.fsm_msg_time_out_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_GEN_TRIG, self.fsm_msg_gen_trig_rcv_handler)
        self.fsm_set(TUP_STM_INIT)
        #START TASK
        self.task_run()

    def fsm_msg_init_rcv_handler(self, msgContent):
        #time.sleep(0.5) #WAIT FOR OTHER TASK STARTUP
        return TUP_SUCCESS;

    def fsm_msg_restart_rcv_handler(self, msgContent):
        self.tup_dbg_print("I am in fsm_msg_restart_rcv_handler = ", msgContent)
        #time.sleep(1)
        msgSnd = {}
        msgSnd['mid'] = TUP_MSGID_GEN_TRIG
        msgSnd['src'] = TUP_TASK_ID_TEST
        msgSnd['dst'] = TUP_TASK_ID_VMCONSL
        msgSnd['content'] = "test> " + str(random.random())
        self.fsm_set(self._STM_ACTIVE)
        self.msg_send_in(msgSnd)
        return TUP_SUCCESS;

    def fsm_msg_time_out_rcv_handler(self, msgContent):
        self.tup_dbg_print("I am in fsm_msg_time_out_rcv_handler = ", msgContent)
        return TUP_SUCCESS;
        
    def fsm_msg_gen_trig_rcv_handler(self, msgContent):
        self.tup_dbg_print("I am in fsm_msg_gen_trig_rcv_handler = ", msgContent)
        self.fsm_set(TUP_STM_INIT)
        return TUP_SUCCESS;
        











#EXAMPLE        
def vm_main_entry():
    myTaskInst = tupTaskVmConsl();
    msg = {}
    while True:
        time.sleep(0.5)
        msg['mid'] = TUP_MSGID_RESTART
        msg['src'] = TUP_TASK_ID_TEST
        msg['dst'] = TUP_TASK_ID_VMCONSL
        msg['content'] = "test> " + str(random.random())
        myTaskInst.msg_send_in(msg)
        
        
        