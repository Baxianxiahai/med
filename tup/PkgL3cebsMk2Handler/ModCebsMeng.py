'''
Created on 2018年12月8日

@author: Administrator
'''

import random
import time
from multiprocessing import Queue, Process
from PkgL1vmHandler.ModVmCfg import *
from PkgL1vmHandler.ModVmLayer import *
from PkgL3cebsMk2Handler.ModCebsCom import *
from PkgL3cebsMk2Handler.ModCebsCfg import *
from PkgL1vmHandler.ModVmConsole import *

class tupTaskMeng(tupTaskTemplate, clsL1_ConfigOpr):
    _STM_ACTIVE = 3

    def __init__(self, glPar):
        tupTaskTemplate.__init__(self, taskid=TUP_TASK_ID_MENG, taskName="TASK_MENG", glTabEntry=glPar)
        #ModVmLayer.TUP_GL_CFG.save_task_by_id(ModVmCfg.TUP_TASK_ID_MENG, self)
        self.fsm_set(TUP_STM_NULL)
        #STM MATRIX
        self.add_stm_combine(TUP_STM_INIT, TUP_MSGID_INIT, self.fsm_msg_init_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_RESTART, self.fsm_com_msg_restart_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_EXIT, self.fsm_com_msg_exit_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TEST, self.fsm_com_msg_test_rcv_handler)
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_TRACE, self.fsm_msg_trace_inc_rcv_handler)
        
        #业务处理部分
        self.add_stm_combine(TUP_STM_COMN, TUP_MSGID_MENG_CLOSE_REQ, self.fsm_msg_close_req_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_MENG_MOTO_COMMAND, self.fsm_msg_moto_cmd_req_rcv_handler)
        self.add_stm_combine(self._STM_ACTIVE, TUP_MSGID_MENG_MOTO_CMD_FB, self.fsm_msg_moto_cmd_resp_rcv_handler)
        
        #START TASK
        self.fsm_set(TUP_STM_INIT)
        self.task_run()

    def fsm_msg_init_rcv_handler(self, msgContent):
        self.fsm_set(self._STM_ACTIVE)
        time.sleep(0.5) #WAIT FOR OTHER TASK STARTUP
        return TUP_SUCCESS;

    def fsm_msg_trace_inc_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_MENG, msgContent)
        return TUP_SUCCESS;
    
    def fsm_msg_close_req_rcv_handler(self, msgContent):
        self.func_clean_working_env()
        return TUP_SUCCESS;

    def fsm_msg_moto_cmd_req_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_MENG_MOTO_COMMAND, TUP_TASK_ID_MOTO, msgContent)
        return TUP_SUCCESS;
    
    def fsm_msg_moto_cmd_resp_rcv_handler(self, msgContent):
        self.msg_send(TUP_MSGID_MENG_MOTO_CMD_FB, TUP_TASK_ID_UI_MENG, msgContent)
        return TUP_SUCCESS;    

    def funcMengLogTrace(self, myString):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_MENG, myString)
        #SAVE INTO MED FILE
        self.medCmdLog(str(myString))
        #PRINT to local
        self.tup_dbg_print(str(myString))
        return
    
    def funcMengErrTrace(self, myString):
        self.msg_send(TUP_MSGID_TRACE, TUP_TASK_ID_UI_MENG, myString)
        #SAVE INTO MED FILE
        self.medErrorLog(str(myString));
        #PRINT to local
        self.tup_err_print(str(myString))
        return        
    
    #业务函数    
    def func_clean_working_env(self):
        pass








